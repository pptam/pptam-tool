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
        # Endpoints (override in config if your API differs)
        self.reserve_path = configuration.get("attack_reserve_path") or "/api/v1/reservation"
        self.cancel_path = configuration.get("attack_cancel_path") or "/api/v1/reservation/cancel"
        self.hotel_id = configuration.get("attack_hotel_id") or "attack-hotel"
        self.concurrency = int(float(configuration.get("attack_concurrency", 30)))
        self.timeout = float(configuration.get("attack_request_timeout_seconds", 5))
        lock_hold = configuration.get("attack_reservation_lock_hold_seconds")
        try:
            self.lock_hold_seconds = max(0.0, float(lock_hold))
        except (TypeError, ValueError):
            self.lock_hold_seconds = 0.15

    def worker(self, end_ts, stop_event):
        session = requests.Session()
        reserve_url = f"{self.base_url}{self.reserve_path}"
        cancel_url = f"{self.base_url}{self.cancel_path}"
        while (time.time() < end_ts) and (not stop_event.is_set()):
            try:
                in_date = f"2020-01-{random.randint(1, 15):02d}"
                out_date = f"2020-01-{random.randint(16, 28):02d}"
                body = {
                    "hotelId": self.hotel_id,
                    "inDate": in_date,
                    "outDate": out_date,
                    "rooms": random.randint(1, 3),
                    "guests": random.randint(1, 4),
                }
                r = session.post(reserve_url, json=body, timeout=self.timeout)
                reservation_id = None
                try:
                    data = r.json() if r is not None else None
                    reservation_id = (data or {}).get("reservationId") or (data or {}).get("id")
                except Exception:
                    pass
                if self.lock_hold_seconds > 0:
                    stop_event.wait(timeout=self.lock_hold_seconds)
                # Immediately cancel (best effort)
                cancel_body = {"hotelId": self.hotel_id}
                if reservation_id is not None:
                    cancel_body["reservationId"] = reservation_id
                session.post(cancel_url, json=cancel_body, timeout=self.timeout)
            except Exception:
                pass

    def run(self, duration_seconds, stop_event):
        logging.info(
            "reservation_churn: starting (target_service=%s, concurrency=%d, hold=%.2fs)",
            self.TARGET_SERVICE,
            self.concurrency,
            self.lock_hold_seconds,
        )
        end_ts = time.time() + duration_seconds
        threads = [threading.Thread(target=self.worker, args=(end_ts, stop_event), daemon=True) for _ in range(self.concurrency)]
        for t in threads:
            t.start()
        for t in threads:
            remaining = max(0.0, end_ts - time.time())
            t.join(timeout=remaining)
        logging.info("reservation_churn: finished")
