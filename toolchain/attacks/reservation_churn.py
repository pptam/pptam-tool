#!/usr/bin/env python3
import threading
import time
import logging
import random
import requests


class Attack:
    """Database lock contention via reservation churn targeting the reservation service."""

    VECTOR_NAME = "reservation_lock_contention"
    TARGET_SERVICE = "reservation"
    RESOURCE_DIMENSIONS = ("cpu", "io", "database")

    def __init__(self, configuration, design_path, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.base_url = (configuration.get("locust_host_url") or "").rstrip("/")
        self.reserve_path = configuration.get("attack_reserve_path") or "/reservation"
        self.concurrency = int(float(configuration.get("attack_concurrency", 30)))
        self.timeout = float(configuration.get("attack_request_timeout_seconds", 5))
        try:
            self.max_rooms = max(1, int(float(configuration.get("attack_reservation_max_rooms", 3))))
        except Exception:
            self.max_rooms = 3
        try:
            self.max_stay_nights = max(1, int(float(configuration.get("attack_reservation_max_stay_nights", 4))))
        except Exception:
            self.max_stay_nights = 4

    def _build_params(self):
        start_day = random.randint(1, 25)
        stay = random.randint(1, self.max_stay_nights)
        in_date = f"2015-04-{start_day:02d}"
        out_day = min(30, start_day + stay)
        out_date = f"2015-04-{out_day:02d}"
        lat = 38.0235 + (random.randint(0, 481) - 240.5) / 1000.0
        lon = -122.095 + (random.randint(0, 325) - 157.0) / 1000.0
        hotel_id = random.randint(1, 80)
        customer = f"load-user-{random.randint(1, 10000)}"
        username = customer
        password = f"{random.randint(1000, 9999)}"
        rooms = random.randint(1, self.max_rooms)
        params = {
            "inDate": in_date,
            "outDate": out_date,
            "lat": f"{lat:.4f}",
            "lon": f"{lon:.4f}",
            "hotelId": str(hotel_id),
            "customerName": customer,
            "username": username,
            "password": password,
            "number": str(rooms),
        }
        return params

    def worker(self, end_ts, stop_event):
        session = requests.Session()
        reserve_url = f"{self.base_url}{self.reserve_path}"
        while (time.time() < end_ts) and (not stop_event.is_set()):
            params = self._build_params()
            try:
                session.post(reserve_url, params=params, timeout=self.timeout)
            except Exception:
                pass

    def run(self, duration_seconds, stop_event):
        logging.info(
            "reservation_churn: starting (target_service=%s, concurrency=%d, max_rooms=%d, max_stay=%d)",
            self.TARGET_SERVICE,
            self.concurrency,
            self.max_rooms,
            self.max_stay_nights,
        )
        end_ts = time.time() + duration_seconds
        threads = [threading.Thread(target=self.worker, args=(end_ts, stop_event), daemon=True) for _ in range(self.concurrency)]
        for t in threads:
            t.start()
        for t in threads:
            remaining = max(0.0, end_ts - time.time())
            t.join(timeout=remaining)
        logging.info("reservation_churn: finished")
