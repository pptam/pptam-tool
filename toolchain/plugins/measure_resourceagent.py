import threading
import requests
import os
import logging
from queue import Queue, Empty
from datetime import datetime
import time

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
            #logging.info("DATA: %s", data)
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
            #logging.info("Containers: %s", containers)

            for proc in containers:
                container_name = proc.get("container_name", "")
                container_id = proc.get("container_id", "")
                pid = proc.get("pid", "")

                self.write_queue.put(
                    f"{now},{container_name},{container_id},{pid}\n"
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
            self.stop_event.wait(interval_seconds)  # allows early stop

    def queue_writer(self):
        logging.info("Waiting for process stats results.")
        file_path = os.path.join(self.output_path, "resourceagent_stats.csv")
        with open(file_path, "w") as f:
            f.write("collected,container_name,container_id,pid\n")
        with open(file_path, "a") as f:
            while True:
                try:
                    item = self.write_queue.get(timeout=1.0)
                    if item is None:  # sentinel -> stop
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
        self.write_queue.put(None)  # sentinel for writer
        if self.worker_thread:
            self.worker_thread.join(timeout=5)
        if self.writer_thread:
            self.writer_thread.join(timeout=5)

def before(current_configuration, design_path, output, test_id):
    global _collector_instance
    _collector_instance = ResourceAgentCollector(current_configuration, output, test_id)
    _collector_instance.start()

def after(current_configuration, design_path, output, test_id):
    global _collector_instance
    if _collector_instance is not None:
        _collector_instance.stop()
        _collector_instance = None
