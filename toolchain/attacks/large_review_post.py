#!/usr/bin/env python3
import threading
import time
import logging
import requests


class Attack:
    def __init__(self, configuration, design_path, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.base_url = (configuration.get("locust_host_url") or "").rstrip("/")
        self.review_path = configuration.get("attack_review_path") or "/api/v1/review"
        self.concurrency = int(float(configuration.get("attack_concurrency", 10)))
        self.timeout = float(configuration.get("attack_request_timeout_seconds", 10))
        size = int(float(configuration.get("attack_large_body_size_bytes", 2 * 1024 * 1024)))
        self.large_content = ("A" * min(size, 10_000_000)).encode("utf-8", errors="ignore")

    def worker(self, end_ts, stop_event):
        session = requests.Session()
        url = f"{self.base_url}{self.review_path}"
        headers = {"Content-Type": "application/octet-stream"}
        while (time.time() < end_ts) and (not stop_event.is_set()):
            try:
                session.post(url, data=self.large_content, headers=headers, timeout=self.timeout)
            except Exception:
                pass

    def run(self, duration_seconds, stop_event):
        logging.info("large_review_post: starting")
        end_ts = time.time() + duration_seconds
        threads = [threading.Thread(target=self.worker, args=(end_ts, stop_event), daemon=True) for _ in range(self.concurrency)]
        for t in threads:
            t.start()
        for t in threads:
            remaining = max(0.0, end_ts - time.time())
            t.join(timeout=remaining)
        logging.info("large_review_post: finished")

