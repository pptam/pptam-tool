import logging
import os
import json
import sched
import threading
from queue import Queue, Empty
from datetime import datetime
import requests

_collector_instance = None


class GlancesSystemStatsCollector:
    def __init__(self, configuration, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.stop_event = threading.Event()
        self.write_queue = Queue()
        self.writer_thread = None
        self.worker_thread = None
        self.csv_fields = None

    def build_base_url(self):
        explicit = self.configuration.get("glances_base_url")
        if explicit:
            base = explicit.strip().rstrip("/")
            if not base.startswith("http://") and not base.startswith("https://"):
                base = f"http://{base}"
            return base
        host = self.configuration.get("glances_host") or self.configuration.get("docker_deploy_ssh_target_machine") or self.configuration.get("target_machine")
        if not host:
            raise ValueError("glances_base_url or glances_host not configured")
        host = str(host).strip()
        if "@" in host:
            host = host.split("@", 1)[1]
        if " " in host:
            host = host.split(" ", 1)[0]
        if not host.startswith("http://") and not host.startswith("https://"):
            host = f"http://{host}"
        if ":" not in host.split("//", 1)[-1]:
            host = f"{host}:61208"
        return host.rstrip("/")

    def http_get_json(self, path):
        base = self.build_base_url()
        url = f"{base}{path}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def collect_from_glances(self):
        cpu = self.http_get_json("/api/3/cpu")
        mem = self.http_get_json("/api/3/mem")
        vmstat = None
        try:
            vmstat = self.http_get_json("/api/3/vmstat")
        except Exception:
            vmstat = None
        data = {}
        if isinstance(cpu, dict):
            if "total" in cpu:
                data["cpu_total_percent"] = float(cpu.get("total") or 0.0)
            for k in ("user", "system", "idle", "iowait"):
                if k in cpu and isinstance(cpu.get(k), (int, float)):
                    data[f"cpu_{k}"] = float(cpu.get(k))
        if isinstance(mem, dict):
            for k_map, src in [("mem_total", "total"), ("mem_available", "available"), ("mem_free", "free"), ("mem_used", "used")]:
                if src in mem:
                    v = mem.get(src)
                    if isinstance(v, (int, float)):
                        data[k_map] = float(v)
            if "total" in mem and "available" in mem and isinstance(mem.get("total"), (int, float)) and isinstance(mem.get("available"), (int, float)) and mem.get("total") > 0:
                data["mem_available_percent"] = float(mem.get("available")) / float(mem.get("total")) * 100.0
        if isinstance(vmstat, dict):
            flat = {}
            stack = [("vmstat", vmstat)]
            while stack:
                prefix, obj = stack.pop()
                if isinstance(obj, dict):
                    for kk, vv in obj.items():
                        new_prefix = f"{prefix}_{kk}"
                        if isinstance(vv, dict):
                            stack.append((new_prefix, vv))
                        elif isinstance(vv, (int, float)):
                            flat[new_prefix] = float(vv)
                elif isinstance(obj, (int, float)):
                    flat[prefix] = float(obj)
            for kk, vv in flat.items():
                data[kk] = vv
        return data

    def collect_once(self):
        try:
            collected_ts = datetime.timestamp(datetime.utcnow())
            metrics = self.collect_from_glances()
            timestamp_ts = collected_ts
            payload = {"collected": collected_ts, "timestamp": timestamp_ts}
            payload.update(metrics)
            self.enqueue_write(payload)
        except Exception:
            logging.exception("Failed to collect metrics from Glances")

    def enqueue_write(self, row_dict):
        try:
            self.write_queue.put(json.dumps(row_dict))
        except Exception:
            pass

    def scheduler_worker(self):
        interval_seconds = int(self.configuration["docker_stats_run_every_number_of_seconds"])
        run_time_seconds = int(self.configuration["run_time_in_seconds"])
        number_of_calls = 1 + (run_time_seconds // interval_seconds)
        scheduler = sched.scheduler()
        for i in range(number_of_calls):
            if self.stop_event.is_set():
                break
            scheduler.enter(i * interval_seconds, 1, self.collect_once)
        if not self.stop_event.is_set():
            scheduler.run()

    def queue_writer(self):
        file_path = os.path.join(self.output_path, "glances_system_stats.csv")
        file_exists = os.path.exists(file_path)
        with open(file_path, "a") as f:
            while not self.stop_event.is_set():
                try:
                    item = self.write_queue.get(timeout=1.0)
                    row = json.loads(item)
                    if self.csv_fields is None:
                        fields = list(row.keys())
                        fields_sorted = ["collected", "timestamp"] + sorted([k for k in fields if k not in ("collected", "timestamp")])
                        self.csv_fields = fields_sorted
                        if not file_exists or os.path.getsize(file_path) == 0:
                            f.write(",".join(self.csv_fields) + "\n")
                    values = [str(row.get(k, "")) for k in self.csv_fields]
                    f.write(",".join(values) + "\n")
                    f.flush()
                except Empty:
                    continue
                except Exception:
                    logging.exception("Failed to write metrics row")
            while True:
                try:
                    item = self.write_queue.get_nowait()
                except Empty:
                    break
                else:
                    try:
                        row = json.loads(item)
                        if self.csv_fields is None:
                            fields = list(row.keys())
                            fields_sorted = ["collected", "timestamp"] + sorted([k for k in fields if k not in ("collected", "timestamp")])
                            self.csv_fields = fields_sorted
                            f.write(",".join(self.csv_fields) + "\n")
                        values = [str(row.get(k, "")) for k in self.csv_fields]
                        f.write(",".join(values) + "\n")
                        f.flush()
                    except Exception:
                        logging.exception("Failed to write metrics row on drain")

    def start(self):
        self.writer_thread = threading.Thread(target=self.queue_writer, daemon=True)
        self.worker_thread = threading.Thread(target=self.scheduler_worker, daemon=True)
        self.writer_thread.start()
        self.worker_thread.start()

    def stop(self):
        self.stop_event.set()
        try:
            self.write_queue.put("")
        except Exception:
            pass


def before(current_configuration, design_path, output, test_id):
    global _collector_instance
    _collector_instance = GlancesSystemStatsCollector(current_configuration, output, test_id)
    _collector_instance.start()


def after(current_configuration, design_path, output, test_id):
    global _collector_instance
    if _collector_instance is not None:
        _collector_instance.stop()
        _collector_instance = None
