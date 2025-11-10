import threading
import requests
import os
import logging
from queue import Queue, Empty
from datetime import datetime
import time
import json

_collector_instance = None


class ResourceAgentCollector:
    def __init__(self, configuration, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.stop_event = threading.Event()
        self.write_queue = Queue()
        self.writer_thread = None
        self.worker_thread = None

    def get_base_url(self):
        host_value = self.configuration.get("resourceagent_hostname")
        if not host_value:
            raise ValueError("RESOURCEAGENT_HOSTNAME not configured")
        if host_value.startswith(("http://", "https://")):
            base = host_value
        else:
            base = f"http://{host_value}"
        if ":" not in base.split("//", 1)[-1]:
            base = f"{base}:7333"
        return base.rstrip("/")

    def fetch_metrics(self):
        url = f"{self.get_base_url()}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        try:
            data = response.json()
            return data
        except ValueError:
            return {"raw_metrics": response.text.splitlines()}

    def collect_batch(self):
        if self.stop_event.is_set():
            return
        try:
            now = round(datetime.utcnow().timestamp())
            data = self.fetch_metrics()
            containers = data.get("containers", [])

            for proc in containers:
                container_name = proc.get("container_name", "")
                container_id = proc.get("container_id", "")
                host_pid = proc.get("host_pid", "")
                container_pids = proc.get("container_pids", [])

                for pid in container_pids:
                    self.write_queue.put(
                        f"{now},{container_name},{container_id},{host_pid},{pid}\n"
                    )
        except Exception:
            logging.exception("Failed to collect resourceagent stats")

    def scheduler_worker(self):
        interval_seconds = int(self.configuration.get("resourceagent_run_every_number_of_seconds", 3))
        run_time_seconds = int(self.configuration.get("run_time_in_seconds", 20))
        end_time = time.time() + run_time_seconds

        logging.info("Collecting process stats in background via Resourceagent.")

        while not self.stop_event.is_set() and time.time() < end_time:
            self.collect_batch()
            self.stop_event.wait(interval_seconds)

    def queue_writer(self):
        logging.info("Waiting for process stats results.")
        file_path = os.path.join(self.output_path, "resourceagent_stats.csv")
        with open(file_path, "w") as f:
            f.write("collected,container_name,container_id,host_pid,container_pid\n")
        with open(file_path, "a") as f:
            while True:
                try:
                    item = self.write_queue.get(timeout=1.0)
                    if item is None:
                        break
                    f.write(item)
                    f.flush()
                except Empty:
                    if self.stop_event.is_set():
                        break
                    continue

    def start(self):
        self.writer_thread = threading.Thread(target=self.queue_writer, daemon=True)
        self.worker_thread = threading.Thread(target=self.scheduler_worker, daemon=True)
        self.writer_thread.start()
        self.worker_thread.start()

    def stop(self):
        self.stop_event.set()
        self.write_queue.put(None)
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        if self.writer_thread:
            self.writer_thread.join(timeout=5)

    def fetch_and_save_download_all(self):
        """
        1) Fetch current state from resourceagent base path (/) and save as docker_pids.json
        2) Call resourceagent /download-all and save returned files into self.output_path
        """
        # ---- Step 1: snapshot current JSON from "/" before download-all ----
        try:
            base_url = self.get_base_url()
            snap_url = f"{base_url}"
            logging.info("Fetching current PID/container snapshot: %s", snap_url)
            snap_resp = requests.get(snap_url, timeout=10)
            snap_resp.raise_for_status()

            try:
                snapshot = snap_resp.json()
            except ValueError:
                snapshot = {"raw": snap_resp.text}

            docker_pids_path = os.path.join(self.output_path, "docker_pids.json")
            with open(docker_pids_path, "w", encoding="utf-8") as fp:
                json.dump(snapshot, fp, indent=2, sort_keys=True)
            logging.info("Saved docker PIDs snapshot: %s", docker_pids_path)
        except Exception:
            logging.exception("Failed to fetch/save docker PID snapshot from '/'")

        # ---- Step 2: call /download-all and save files ----
        try:
            url = f"{self.get_base_url()}/download-all"
            logging.info("Calling resourceagent /download-all: %s", url)
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            try:
                payload = resp.json()
            except ValueError:
                logging.error("resourceagent /download-all returned non-JSON response")
                return

            files = payload.get("files", {}) or {}
            if not files:
                logging.info("resourceagent /download-all returned no files")
                return

            for fname, meta in files.items():
                safe = os.path.basename(fname)
                path = os.path.join(self.output_path, safe)
                content = meta.get("content", "")
                try:
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(content)
                    logging.info("Saved resourceagent file: %s", path)
                except Exception:
                    logging.exception("Failed to save resourceagent file %s", path)
        except Exception:
            logging.exception("Error during /download-all fetch/save")


# =====================================================
# === Hooks called before / after test runs ===
# =====================================================

def before(current_configuration, design_path, output, test_id):
    """
    Called before the test starts.
    - Calls /reset on the ResourceAgent to ensure a clean state
    - Starts background collection
    """
    global _collector_instance

    try:
        # --- Call /reset before collecting ---
        host = current_configuration.get("resourceagent_hostname")
        if not host:
            raise ValueError("Missing resourceagent_hostname in configuration")

        if not host.startswith(("http://", "https://")):
            host = f"http://{host}"
        if ":" not in host.split("//", 1)[-1]:
            host = f"{host}:7333"
        reset_url = f"{host.rstrip('/')}/reset"

        logging.info("Resetting ResourceAgent state: %s", reset_url)
        resp = requests.get(reset_url, timeout=15)
        logging.info("Reset response [%s]: %s", resp.status_code, resp.text[:200])
    except Exception:
        logging.exception("Failed to call /reset on ResourceAgent before test start")

    # --- Start background collector ---
    _collector_instance = ResourceAgentCollector(current_configuration, output, test_id)
    _collector_instance.start()


def after(current_configuration, design_path, output, test_id):
    """
    Called after the test ends.
    - Fetches all PID logs via /download-all
    - Stops the collector threads
    """
    global _collector_instance
    if _collector_instance is not None:
        try:
            _collector_instance.fetch_and_save_download_all()
        except Exception:
            logging.exception("Error fetching /download-all in after()")
        _collector_instance.stop()
        _collector_instance = None

