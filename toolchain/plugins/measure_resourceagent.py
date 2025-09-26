import threading
import requests
import os
import logging
from queue import Queue, Empty
from datetime import datetime

class ResourceAgent:
    def __init__(self, configuration, output_path):
        self.configuration = configuration
        self.output_path = output_path
        self.stopevent = threading.Event()
        self.writequeue = Queue()
        self.writerthread = None
        self.workerthread = None

    def get_base_url(self):
        host = self.configuration.get("resourceagent_hostname")
        if not host:
            raise ValueError("RESOURCEAGENT_HOSTNAME not configured")
        base = host if host.startswith("http") else f"http://{host}"
        if ":" not in base.split("//", 1)[-1]:
            base += ":8080"
        return base.rstrip("/")

    def fetch_metrics(self):
        url = f"{self.get_base_url()}/"
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def collect_batch(self):
        if self.stopevent.is_set():
            return
        try:
            now = round(datetime.utcnow().timestamp())
            data = self.fetch_metrics()
            for proc in data.get("processes", []):
                pid = proc.get("pid", "")
                cpusec = proc.get("cpuseconds", 0.0)
                mem = proc.get("memorybytes", 0.0)
                disk = proc.get("diskbytes", 0.0)
                energy = proc.get("energyjoules", 0.0)
                self.writequeue.put(f"{now},{pid},{cpusec},{mem},{disk},{energy}\n")
        except Exception as e:
            logging.warning(f"Failed batch: {e}")

    def scheduler_worker(self):
        interval = int(self.configuration.get("collect_every_seconds", 10))
        while not self.stopevent.is_set():
            self.collect_batch()
            threading.Event().wait(interval)

    def queue_writer(self):
        path = os.path.join(self.output_path, "resourceagentprocess.csv")
        with open(path, "w") as f:
            f.write("collected,pid,cpuseconds,memorybytes,diskbytes,energyjoules\n")
        with open(path, "a") as f:
            while not self.stopevent.is_set():
                try:
                    line = self.writequeue.get(timeout=1.0)
                    f.write(line)
                    f.flush()
                except Empty:
                    continue

    def start(self):
        self.writerthread = threading.Thread(target=self.queue_writer, daemon=True)
        self.workerthread = threading.Thread(target=self.scheduler_worker, daemon=True)
        self.writerthread.start()
        self.workerthread.start()

    def stop(self):
        self.stopevent.set()
        self.writequeue.put("")

# Example usage:
# config = {"endpoint_hostname": "localhost", "collect_every_seconds": 5}
# agent = ResourceAgent(config, "/tmp")
# agent.start()
# ...wait or run forever...
# agent.stop()

