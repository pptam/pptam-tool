#!/usr/bin/env python3
import threading
import time
import logging
import random
import requests
import urllib.parse as up


class Attack:
    def __init__(self, configuration, design_path, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.base_url = (configuration.get("locust_host_url") or "").rstrip("/")
        self.path = configuration.get("attack_search_path") or "/api/v1/search"
        self.concurrency = int(float(configuration.get("attack_concurrency", 40)))
        self.timeout = float(configuration.get("attack_request_timeout_seconds", 10))
        self.page_size = int(float(configuration.get("attack_search_page_size", 500)))

    def _build_query(self):
        # Randomly combine many filters and sorts
        params = {
            "q": random.choice(["beach", "city", "mountain", "spa", "resort", "luxury", "budget"]),
            "pageSize": str(self.page_size),
            "sort": random.choice(["price,asc", "price,desc", "rating,desc", "distance,asc"]),
            "amenities": ",".join(random.sample(["wifi", "pool", "parking", "gym", "spa", "bar", "restaurant"], k=4)),
            "filters": ",".join(random.sample(["non_smoking", "pet_friendly", "breakfast", "free_cancellation", "pay_at_hotel"], k=3)),
            "date": random.choice(["2020-01-01", "2020-06-01", "2020-12-01"]),
        }
        return up.urlencode(params, doseq=True)

    def worker(self, end_ts, stop_event):
        session = requests.Session()
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate"
        }
        while (time.time() < end_ts) and (not stop_event.is_set()):
            url = f"{self.base_url}{self.path}?{self._build_query()}"
            try:
                session.get(url, headers=headers, timeout=self.timeout)
            except Exception:
                pass

    def run(self, duration_seconds, stop_event):
        logging.info("expensive_filter_queries: starting")
        end_ts = time.time() + duration_seconds
        threads = [threading.Thread(target=self.worker, args=(end_ts, stop_event), daemon=True) for _ in range(self.concurrency)]
        for t in threads:
            t.start()
        for t in threads:
            remaining = max(0.0, end_ts - time.time())
            t.join(timeout=remaining)
        logging.info("expensive_filter_queries: finished")

