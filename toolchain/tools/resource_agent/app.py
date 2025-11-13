import json
import threading
import time
import docker
import subprocess
import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from docker.errors import NotFound

# --- Configuration ---
PORT = 7333
REFRESH_INTERVAL_SECONDS = 1  # seconds between checks
PID_LOG_DIR = "pid-log"       # Directory to store pid log files
RESET_SUPPRESS_SECONDS = 2    # Pause polling briefly after a reset

# Ensure pid-log directory exists
os.makedirs(PID_LOG_DIR, exist_ok=True)

# --- Shared data store ---
container_data_store = {"containers": []}
data_lock = threading.Lock()

pid_manager = None
_last_reset_monotonic = 0.0
logger = logging.getLogger(__name__)


# =====================================================
# === PID and Container State Manager ===
# =====================================================
class PIDManager:
    def __init__(self):
        # container_id -> {"name": str, "pids": {pid_number: pid_info}}
        self.containers = {}

    def reset(self):
        # Stop any powerjoular processes we spawned and clear state
        for cid, cdata in list(self.containers.items()):
            for pid, entry in list(cdata["pids"].items()):
                proc = entry.get("process")
                if proc and proc.poll() is None:
                    try:
                        proc.terminate()
                        proc.wait(timeout=2)
                    except Exception:
                        logger.exception("Failed to terminate PID %s cleanly", pid)
                        try:
                            proc.kill()
                        except Exception:
                            logger.exception("Failed to kill PID %s", pid)
                entry["status"] = "END"
        self.containers.clear()

    def update_containers(self, docker_containers):
        """
        docker_containers = [
            {"container_name": str, "container_id": str,
             "host_pid": int, "container_pids": [int, ...]}
        ]
        """
        active_containers = {c["container_id"]: c for c in docker_containers}

        # --- Handle new or updated containers ---
        for cid, cinfo in active_containers.items():
            cname = cinfo["container_name"]
            if cid not in self.containers:
                self.containers[cid] = {"name": cname, "pids": {}}

            all_pids = [("host", cinfo["host_pid"])] + [
                ("container", pid) for pid in cinfo["container_pids"]
            ]
            current_pids = {p for _, p in all_pids if p is not None}

            # Detect NEW PIDs
            for ptype, pid in all_pids:
                if pid is None:
                    continue
                if pid not in self.containers[cid]["pids"]:
                    filename = os.path.join(PID_LOG_DIR, f"pid_{cid[:8]}_{pid}")
                    self.containers[cid]["pids"][pid] = {
                        "type": ptype,
                        "number": pid,
                        "status": "NEW",
                        "process": None,
                        "filename": filename
                    }
                    logger.debug("New PID %s (%s) in %s (%s)", pid, ptype, cname, cid[:8])
                    self._handle_new_pid(cid, pid)

            # Detect vanished PIDs
            for old_pid in list(self.containers[cid]["pids"].keys()):
                if old_pid not in current_pids:
                    entry = self.containers[cid]["pids"][old_pid]
                    if entry["status"] not in ["CLOSING", "END"]:
                        entry["status"] = "CLOSING"
                        logger.debug("PID %s from %s (%s) is closing", old_pid, cname, cid[:8])
                        self._handle_closing_pid(cid, old_pid)

        # --- Handle containers that disappeared entirely ---
        for cid in list(self.containers.keys()):
            if cid not in active_containers:
                for pid in list(self.containers[cid]["pids"].keys()):
                    entry = self.containers[cid]["pids"][pid]
                    if entry["status"] not in ["CLOSING", "END"]:
                        entry["status"] = "CLOSING"
                        logger.debug("Container %s removed; closing PID %s", cid[:8], pid)
                        self._handle_closing_pid(cid, pid)

    # --------------------------------------------
    # Handle new PIDs (start powerjoular)
    # --------------------------------------------
    def _handle_new_pid(self, cid, pid):
        entry = self.containers[cid]["pids"][pid]
        filename = entry["filename"]
        short_id = cid[:8]
        try:
            # Remove -t flag to avoid timeout issues, redirect output to /dev/null to prevent pipe buffer issues
            cmd = ["sudo", "powerjoular", "-p", str(pid), "-f", filename]
            with open(os.devnull, 'w') as devnull:
                proc = subprocess.Popen(cmd, stdout=devnull, stderr=devnull)
            entry["process"] = proc
            entry["status"] = "RUNNING"
            logger.info("Started powerjoular for PID %s (%s)", pid, short_id)
        except Exception:
            entry["status"] = "ERROR"
            logger.exception("Could not start powerjoular for PID %s (%s)", pid, short_id)

    # --------------------------------------------
    # Handle closing PIDs
    # --------------------------------------------
    def _handle_closing_pid(self, cid, pid):
        entry = self.containers[cid]["pids"][pid]
        proc = entry.get("process")
        if proc and proc.poll() is None:
            logger.info("Terminating powerjoular for PID %s (%s)", pid, cid[:8])
            proc.terminate()
            threading.Thread(
                target=self._wait_for_close, args=(cid, pid, proc), daemon=True
            ).start()
        else:
            entry["status"] = "END"

    def _wait_for_close(self, cid, pid, proc):
        try:
            proc.wait(timeout=5)
            logger.debug("Powerjoular for PID %s exited cleanly", pid)
        except subprocess.TimeoutExpired:
            logger.warning("Force closing powerjoular for PID %s", pid)
            proc.kill()
        finally:
            self.containers[cid]["pids"][pid]["status"] = "END"

    # --------------------------------------------
    # Return JSON-safe snapshot
    # --------------------------------------------
    def get_data(self):
        containers = []
        for cid, cdata in self.containers.items():
            containers.append({
                "container_name": cdata["name"],
                "container_id": cid,
                "pids": [
                    {
                        "type": p["type"],
                        "number": p["number"],
                        "status": p["status"],
                        "filename": p["filename"]
                    }
                    for p in cdata["pids"].values()
                ]
            })
        return containers


# =====================================================
# === Docker Polling Thread ===
# =====================================================
def get_container_pids(container):
    """Return host PID and list of container PIDs."""
    pids = []
    try:
        top_result = container.top()
        processes = top_result.get("Processes", [])
        pid_index = top_result["Titles"].index("PID") if "PID" in top_result["Titles"] else None
        if pid_index is not None:
            pids = [int(proc[pid_index]) for proc in processes]
    except Exception:
        logger.exception("Could not get PIDs for %s", container.short_id)
    host_pid = container.attrs["State"].get("Pid")
    return host_pid, pids


def fetch_docker_info(pid_manager_obj):
    global _last_reset_monotonic
    logger.info("Starting Docker monitoring thread")
    try:
        client = docker.from_env()
    except Exception:
        logger.exception("Could not connect to Docker daemon")
        with data_lock:
            container_data_store["error"] = "Docker not available"
        return

    while True:
        try:
            # Skip updates briefly after a reset, so UI doesn't repopulate instantly
            if time.monotonic() - _last_reset_monotonic < RESET_SUPPRESS_SECONDS:
                time.sleep(REFRESH_INTERVAL_SECONDS)
                continue

            running = client.containers.list()
            temp_data = []
            for c in running:
                host_pid, container_pids = get_container_pids(c)
                temp_data.append({
                    "container_name": c.name,
                    "container_id": c.id,
                    "host_pid": host_pid,
                    "container_pids": container_pids
                })

            pid_manager_obj.update_containers(temp_data)

            # Update shared structure for HTTP
            with data_lock:
                container_data_store["containers"] = pid_manager_obj.get_data()
                if "error" in container_data_store:
                    del container_data_store["error"]

        except Exception:
            logger.exception("Docker fetch loop failed")
            with data_lock:
                container_data_store["error"] = "Polling failure; see logs for details"
                container_data_store["containers"] = []

        time.sleep(REFRESH_INTERVAL_SECONDS)


# =====================================================
# === Flask App ===
# =====================================================
app = Flask(__name__)

@app.route('/')
@app.route('/data')
def get_data():
    with data_lock:
        return jsonify(container_data_store)

@app.route('/file/<filename>')
def get_file_content(filename):
    try:
        file_path = os.path.join(PID_LOG_DIR, filename)
        # Ensure the file is within pid-log directory to prevent directory traversal
        if not os.path.abspath(file_path).startswith(os.path.abspath(PID_LOG_DIR)):
            return jsonify({"error": "Invalid file path"}), 400

        if not os.path.exists(file_path):
            return jsonify({"error": "File not found"}), 404

        with open(file_path, 'r') as file:
            content = file.read()

        keep_file = request.args.get('keep', 'false').lower() == 'true'
        if not keep_file:
            os.remove(file_path)

        return jsonify({
            "filename": filename,
            "content": content,
            "deleted": not keep_file
        })
    except Exception:
        logger.exception("Failed to serve file %s", filename)
        return jsonify({"error": "Failed to retrieve file"}), 500

@app.route('/files')
def list_files():
    try:
        files = [f for f in os.listdir(PID_LOG_DIR) if os.path.isfile(os.path.join(PID_LOG_DIR, f))]
        return jsonify({"files": files})
    except Exception:
        logger.exception("Failed to list pid-log files")
        return jsonify({"error": "Failed to list files"}), 500

@app.route('/download-all')
def download_all_files():
    try:
        files = [f for f in os.listdir(PID_LOG_DIR) if os.path.isfile(os.path.join(PID_LOG_DIR, f))]
        files_data = {
            "timestamp": datetime.now().isoformat(),
            "files": {}
        }

        if files:
            for filename in sorted(files):
                file_path = os.path.join(PID_LOG_DIR, filename)
                with open(file_path, 'r') as f:
                    content = f.read()
                parts = filename.split('_')
                files_data["files"][filename] = {
                    "content": content,
                    "container_id": parts[1] if len(parts) > 1 else None,
                    "pid": parts[2] if len(parts) > 2 else None
                }
            files_data["files_deleted"] = False  # no deletion here
        else:
            files_data["error"] = "No files found in pid-log directory"
            files_data["files_deleted"] = False

        return jsonify(files_data)

    except Exception:
        logger.exception("Failed to download pid-log files")
        return jsonify({"error": "Failed to download files"}), 500

@app.route('/reset', methods=['POST', 'GET'])
def reset_state():
    """
    Reset the service:
      - terminate powerjoular processes and clear PID manager state
      - clear pid-log directory contents
      - clear HTTP snapshot (container_data_store)
      - briefly suppress polling loop so UI won't repopulate instantly
    """
    global _last_reset_monotonic

    killed = 0
    files_deleted = 0
    errors = []

    # 1) Stop processes & clear PID state
    try:
        if pid_manager is not None:
            for cdata in list(pid_manager.containers.values()):
                for entry in list(cdata["pids"].values()):
                    proc = entry.get("process")
                    if proc and proc.poll() is None:
                        killed += 1
            pid_manager.reset()
    except Exception as exc:
        logger.exception("pid_manager.reset() failed")
        errors.append(f"pid_manager.reset() failed: {exc}")

    # 2) Clear pid-log directory
    try:
        for fn in os.listdir(PID_LOG_DIR):
            path = os.path.join(PID_LOG_DIR, fn)
            if os.path.isfile(path):
                try:
                    os.remove(path)
                    files_deleted += 1
                except Exception as e:
                    logger.exception("Failed deleting pid-log file %s", fn)
                    errors.append(f"delete {fn} failed: {e}")
    except Exception as exc:
        logger.exception("Listing pid-log failed during reset")
        errors.append(f"listing pid-log failed: {exc}")

    # 3) Clear HTTP snapshot
    try:
        with data_lock:
            container_data_store["containers"] = []
            if "error" in container_data_store:
                del container_data_store["error"]
    except Exception as exc:
        logger.exception("Failed clearing container data store during reset")
        errors.append(f"clear container_data_store failed: {exc}")

    # 4) Suppress immediate repopulation
    _last_reset_monotonic = time.monotonic()

    return jsonify({
        "status": "ok",
        "powerjoular_processes_terminated": killed,
        "pid_log_files_deleted": files_deleted,
        "errors": errors
    })

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


# =====================================================
# === Main ===
# =====================================================
if __name__ == "__main__":
    pid_manager = PIDManager()
    thread = threading.Thread(target=fetch_docker_info, args=(pid_manager,), daemon=True)
    thread.start()
    app.run(host='0.0.0.0', port=PORT)
