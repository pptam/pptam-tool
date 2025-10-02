#!/usr/bin/env python3
import logging
import os
import sched
import threading
from queue import Queue, Empty
from datetime import datetime
import dateutil.parser
import requests
import re
import yaml  # NEW: read docker-compose.yml

_collector_instance = None


class CAdvisorCollector:
    def __init__(self, configuration, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.stop_event = threading.Event()
        self.write_queue = Queue()
        self.host_write_queue = Queue()
        self.writer_thread = None
        self.worker_thread = None
        self.host_writer_thread = None
        # cache compose services
        self._compose_services = None

    # ---------------------- shared / host helpers (unchanged) ----------------------

    def get_cadvisor_base_url(self):
        host_value = self.configuration.get("cadvisor_hostname")
        if not host_value:
            raise ValueError("CADVISOR_HOSTNAME not configured")
        host_value = host_value.strip()
        if host_value.startswith("http://") or host_value.startswith("https://"):
            base = host_value
        else:
            base = f"http://{host_value}"
        if ":" not in base.split("//", 1)[-1]:
            base = f"{base}:8080"
        return base.rstrip("/")

    def calculate_cpu_percent_from_cadvisor_samples(self, previous_sample, current_sample):
        try:
            prev_total = float(previous_sample.get("cpu", {}).get("usage", {}).get("total", 0.0))
            curr_total = float(current_sample.get("cpu", {}).get("usage", {}).get("total", 0.0))
            prev_ts = previous_sample.get("timestamp")
            curr_ts = current_sample.get("timestamp")
            if not prev_ts or not curr_ts:
                return 0.0
            prev_dt = dateutil.parser.isoparse(prev_ts)
            curr_dt = dateutil.parser.isoparse(curr_ts)
            interval_ns = max((curr_dt - prev_dt).total_seconds(), 0.0) * 1e9
            if interval_ns <= 0.0:
                return 0.0
            cpu_delta = max(curr_total - prev_total, 0.0)
            percent = cpu_delta / interval_ns * 100.0
            return percent
        except Exception:
            logging.exception("Failed to calculate CPU percent from cAdvisor samples")
            return 0.0

    def collect_host_from_cadvisor(self, collection_timestamp):
        try:
            host_entry = self.get_host_container_stats()
            stats_list = host_entry.get("stats", [])
            if len(stats_list) < 2:
                return
            previous_sample = stats_list[-2]
            current_sample = stats_list[-1]
            cpu_percent = self.calculate_cpu_percent_from_cadvisor_samples(previous_sample, current_sample)
            mem_usage = int(current_sample.get("memory", {}).get("usage", 0))
            mem_limit = int(current_sample.get("memory", {}).get("limit", 0))
            a = f"{cpu_percent:.2f}"
            c = f"{float(mem_usage):.2f}"
            d = f"{float(mem_limit):.2f}"
            host_label = self.get_machine_hostname()
            col_ts = round(collection_timestamp)
            sample_ts = round(datetime.timestamp(dateutil.parser.isoparse(current_sample.get('timestamp'))))
            self.host_write_queue.put(f"{col_ts},{sample_ts},{host_label},{a},{c},{d}\n")
        except Exception:
            logging.exception("Failed to collect cAdvisor stats for host")

    def list_cadvisor_containers(self):
        base = self.get_cadvisor_base_url()
        url = f"{base}/api/v1.3/subcontainers"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def normalize_service_name(self, raw_name):
        service_name = raw_name
        expected_prefix = f"{self.test_identifier}_"
        if service_name.startswith(expected_prefix):
            service_name = service_name[len(expected_prefix):]
        first_dot = service_name.find(".")
        if first_dot > 0:
            service_name = service_name[:first_dot]
        return service_name

    def match_containers_to_watch(self, containers):
        # kept for backward compatibility; no longer used by docker stats path
        wanted = set(self.configuration["cadvisor_containers"].split())
        for entry in containers:
            aliases = entry.get("aliases") or []
            if not aliases:
                cgroup_name = entry.get("name") or ""
                raw_name = cgroup_name.split("/")[-1]
            else:
                raw_name = aliases[0]
            service_name = self.normalize_service_name(raw_name)
            if ("all" in wanted) or (service_name in wanted):
                if f"!{service_name}" in wanted:
                    continue
                yield service_name, entry

    def get_host_container_stats(self):
        base = self.get_cadvisor_base_url()
        url = f"{base}/api/v1.3/containers"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_machine_info(self):
        base = self.get_cadvisor_base_url()
        url = f"{base}/api/v1.3/machine"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_docker_containers_map(self):
        base = self.get_cadvisor_base_url()
        url = f"{base}/api/v1.3/docker/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    def get_machine_hostname(self):
        try:
            data = self.get_machine_info()
            return data.get("machineInfo", {}).get("name") or data.get("name") or "host"
        except Exception:
            return "host"

    # ---------------------- NEW: compose-aware docker stats ----------------------

    def _compose_file_path(self):
        base_folder = self.configuration.get("docker_deploy_ssh_target_folder")
        if not base_folder:
            raise ValueError("docker_deploy_ssh_target_folder not configured")
        return os.path.join(base_folder, "docker-compose.yml")

    def _load_compose_services(self):
        if self._compose_services is not None:
            return self._compose_services
        compose_path = self._compose_file_path()
        with open(compose_path, "r", encoding="utf-8") as f:
            doc = yaml.safe_load(f) or {}
        services = list((doc.get("services") or {}).keys())
        self._compose_services = set(services)
        logging.info("Compose services loaded: %s", sorted(self._compose_services))
        return self._compose_services

    @staticmethod
    def _alias_matches_service(alias: str, service: str) -> bool:
        """
        Token-aware match so 'frontend' matches 'project-frontend-1' and 'project_frontend_1'
        without accidental overmatching.
        """
        s = re.escape(service)
        patterns = [
            rf"(?:^|[-_]){s}(?:[-_]\d+)?$",       # ...-service-1 or _service_1 or exactly service
            rf"(?:^|[-_]){s}(?:[-_])",            # service followed by sep
            rf"(?:^){s}(?:[-_])",                 # starts with service-
            rf"(?:[-_]){s}(?:$)",                 # ends with -service
        ]
        for pat in patterns:
            if re.search(pat, alias):
                return True
        return service in alias  # fallback

    def _container_matches_any_service(self, aliases, services) -> list:
        matches = []
        for svc in services:
            if any(self._alias_matches_service(a, svc) for a in (aliases or [])):
                matches.append(svc)
        return matches

    @staticmethod
    def _safe_int(x, default=0):
        try:
            return int(x)
        except Exception:
            try:
                return int(float(x))
            except Exception:
                return default

    def _compute_compose_metrics(self, info: dict):
        """
        Same measures as last script:
         - cpu_percent normalized by sane core limit or host cores
         - memory_percent, usage/limit
         - net totals + bytes/s rates
         - fs capacity/usage/% and read/write time totals
        Returns dict with all fields + the latest sample timestamp and window_seconds.
        """
        spec = info.get("spec", {}) or {}
        stats = info.get("stats", []) or []
        if len(stats) < 2:
            return None

        prev_s = stats[-2]
        curr_s = stats[-1]

        # Δt
        t_prev = dateutil.parser.isoparse(prev_s["timestamp"])
        t_curr = dateutil.parser.isoparse(curr_s["timestamp"])
        dt = max((t_curr - t_prev).total_seconds(), 1e-6)

        # CPU
        cpu_prev = self._safe_int(((prev_s.get("cpu", {}) or {}).get("usage", {}) or {}).get("total", 0))
        cpu_curr = self._safe_int(((curr_s.get("cpu", {}) or {}).get("usage", {}) or {}).get("total", 0))
        d_cpu = max(0, cpu_curr - cpu_prev)

        cpu_spec = spec.get("cpu", {}) or {}
        raw_limit = cpu_spec.get("limit", 0) or 0
        if isinstance(raw_limit, (int, float)) and 0 < float(raw_limit) <= 128:
            cpu_cores_ref = float(raw_limit)
        else:
            try:
                cpu_cores_ref = float(os.cpu_count() or 1)
            except Exception:
                cpu_cores_ref = 1.0
        cpu_percent = (d_cpu / (dt * cpu_cores_ref * 1e9)) * 100.0

        # Memory
        mem_last = (curr_s.get("memory", {}) or {})
        mem_usage = self._safe_int(mem_last.get("usage", 0))
        mem_spec = spec.get("memory", {}) or {}
        if mem_spec.get("limit", 0):
            mem_limit = self._safe_int(mem_spec["limit"])
        else:
            mem_limit = self._safe_int(mem_last.get("limit", 0))
        mem_percent = (mem_usage / mem_limit * 100.0) if mem_limit > 0 else None

        # Network totals + throughput
        net_prev = (prev_s.get("network", {}) or {})
        net_curr = (curr_s.get("network", {}) or {})
        rx_prev = self._safe_int(net_prev.get("rx_bytes", 0))
        tx_prev = self._safe_int(net_prev.get("tx_bytes", 0))
        rx_total = self._safe_int(net_curr.get("rx_bytes", 0))
        tx_total = self._safe_int(net_curr.get("tx_bytes", 0))
        rx_rate = max(0, rx_total - rx_prev) / dt
        tx_rate = max(0, tx_total - tx_prev) / dt

        # Filesystem (aggregate)
        fs_last = (curr_s.get("filesystem", []) or [])
        fs_capacity = 0
        fs_usage = 0
        fs_read_time_total = 0
        fs_write_time_total = 0
        for fs in fs_last:
            fs_capacity += self._safe_int(fs.get("capacity", 0))
            fs_usage += self._safe_int(fs.get("usage", 0))
            fs_read_time_total += self._safe_int(fs.get("read_time", 0))
            fs_write_time_total += self._safe_int(fs.get("write_time", 0))
        fs_usage_percent = (fs_usage / fs_capacity * 100.0) if fs_capacity > 0 else None

        return {
            "sample_ts": t_curr,
            "window_seconds": dt,
            "cpu_percent": cpu_percent,
            "cpu_cores_ref": cpu_cores_ref,
            "cpu_delta_ns": d_cpu,
            "memory_percent": mem_percent,
            "memory_usage_bytes": mem_usage,
            "memory_limit_bytes": mem_limit if mem_limit else 0,
            "net_rx_total_bytes": rx_total,
            "net_tx_total_bytes": tx_total,
            "net_rx_rate_Bps": rx_rate,
            "net_tx_rate_Bps": tx_rate,
            "fs_capacity_bytes": fs_capacity,
            "fs_usage_bytes": fs_usage,
            "fs_usage_percent": fs_usage_percent,
            "fs_read_time_total": fs_read_time_total,
            "fs_write_time_total": fs_write_time_total,
        }

    def _collect_compose_containers_once(self, collection_timestamp):
        """
        Read compose services, fetch /api/v1.3/docker/, match by alias, compute metrics,
        and enqueue CSV rows (container CSV only). Host path is handled elsewhere.
        """
        try:
            services = self._load_compose_services()
        except Exception:
            logging.exception("Failed to load docker-compose services")
            return

        try:
            docker_map = self.get_docker_containers_map()
        except Exception:
            logging.exception("Failed to fetch docker containers map")
            return

        for entry in docker_map.values():
            aliases = entry.get("aliases") or []
            if not aliases:
                continue
            matched_services = self._container_matches_any_service(aliases, services)
            if not matched_services:
                continue

            # Compute metrics once per container
            metrics = self._compute_compose_metrics(entry)
            if metrics is None:
                continue

            col_ts = round(collection_timestamp)
            sample_ts = round(datetime.timestamp(metrics["sample_ts"]))
            window_seconds = metrics["window_seconds"]

            # Write one row per matched service (normally only one)
            for svc in matched_services:
                # Enqueue a rich CSV row (same metrics as last script)
                row = (
                    f"{col_ts},"
                    f"{sample_ts},"
                    f"{svc},"
                    f"{metrics['cpu_percent']:.3f},"
                    f"{metrics['cpu_cores_ref']:.3f},"
                    f"{metrics['cpu_delta_ns']},"
                    f"{(metrics['memory_percent'] if metrics['memory_percent'] is not None else 0):.3f},"
                    f"{metrics['memory_usage_bytes']},"
                    f"{metrics['memory_limit_bytes']},"
                    f"{metrics['net_rx_total_bytes']},"
                    f"{metrics['net_tx_total_bytes']},"
                    f"{metrics['net_rx_rate_Bps']:.3f},"
                    f"{metrics['net_tx_rate_Bps']:.3f},"
                    f"{metrics['fs_capacity_bytes']},"
                    f"{metrics['fs_usage_bytes']},"
                    f"{(metrics['fs_usage_percent'] if metrics['fs_usage_percent'] is not None else 0):.3f},"
                    f"{metrics['fs_read_time_total']},"
                    f"{metrics['fs_write_time_total']},"
                    f"{window_seconds:.3f}"
                    "\n"
                )
                self.write_queue.put(row)

    # ---------------------- batch / scheduler ----------------------

    def collect_batch_via_cadvisor(self):
        if self.stop_event.is_set():
            return
        try:
            collection_timestamp = datetime.timestamp(datetime.utcnow())

            # NEW: compose-aware docker container collection (rich metrics)
            self._collect_compose_containers_once(collection_timestamp)

            # Host collection (unchanged)
            threading.Thread(
                target=self.collect_host_from_cadvisor,
                args=(collection_timestamp,),
                daemon=True
            ).start()

        except Exception:
            logging.exception("Failed to collect batch via cAdvisor")

    def scheduler_worker(self):
        logging.info("Collecting container stats in background via cAdvisor.")
        interval_seconds = int(self.configuration["cadvisor_run_every_number_of_seconds"])
        run_time_seconds = int(self.configuration["run_time_in_seconds"])
        number_of_calls = 1 + (run_time_seconds // interval_seconds)
        logging.info(f"Scheduling container stats for #{number_of_calls} times.")
        scheduler = sched.scheduler()
        for i in range(number_of_calls):
            if self.stop_event.is_set():
                break
            logging.info(f"Scheduling container stats after #{i * interval_seconds} seconds.")
            scheduler.enter(i * interval_seconds, 1, self.collect_batch_via_cadvisor)
        if not self.stop_event.is_set():
            scheduler.run()

    # ---------------------- writers ----------------------

    def container_queue_writer(self):
        logging.info("Waiting for container stats results.")
        file_path = os.path.join(self.output_path, "cadvisor_container.csv")
        # UPDATED HEADER: rich metrics like the last script
        with open(file_path, "w") as f:
            f.write(
                "collected,timestamp,service,"
                "cpu_percent,cpu_cores_ref,cpu_delta_ns,"
                "memory_percent,memory_usage_bytes,memory_limit_bytes,"
                "net_rx_total_bytes,net_tx_total_bytes,net_rx_rate_Bps,net_tx_rate_Bps,"
                "fs_capacity_bytes,fs_usage_bytes,fs_usage_percent,fs_read_time_total,fs_write_time_total,"
                "window_seconds\n"
            )
        with open(file_path, "a") as f:
            while not self.stop_event.is_set():
                try:
                    item = self.write_queue.get(timeout=1.0)
                    f.write(item)
                    f.flush()
                except Empty:
                    continue
            while True:
                try:
                    item = self.write_queue.get_nowait()
                except Empty:
                    break
                else:
                    f.write(item)
                    f.flush()

    def host_queue_writer(self):
        # UNCHANGED
        logging.info("Waiting for host stats results.")
        file_path = os.path.join(self.output_path, "cadvisor_host.csv")
        with open(file_path, "w") as f:
            f.write("collected,timestamp,host,cpu_usage_percent,memory_usage,memory_limit\n")
        with open(file_path, "a") as f:
            while not self.stop_event.is_set():
                try:
                    item = self.host_write_queue.get(timeout=1.0)
                    f.write(item)
                    f.flush()
                except Empty:
                    continue
            while True:
                try:
                    item = self.host_write_queue.get_nowait()
                except Empty:
                    break
                else:
                    f.write(item)
                    f.flush()

    # ---------------------- configuration CSVs (unchanged) ----------------------

    def write_host_configuration_csv(self):
        try:
            data = self.get_machine_info()
            info = data.get("machineInfo", data)
            num_cpus = info.get("num_cores") or info.get("numCores") or info.get("num_cpus") or 0
            memory_bytes = info.get("memory_capacity") or info.get("memoryCapacity") or 0
            host_entry = self.get_host_container_stats()
            stats_list = host_entry.get("stats", []) if isinstance(host_entry, dict) else []
            if len(stats_list) > 0:
                current_sample = stats_list[-1]
                memory_usage_bytes = int(current_sample.get("memory", {}).get("usage", 0))
            else:
                memory_usage_bytes = 0
            file_path = os.path.join(self.output_path, "cadvisor_host_configuration.csv")
            with open(file_path, "w") as f:
                f.write("key,value\n")
                f.write(f"number_of_cpus,{int(num_cpus)}\n")
                f.write(f"memory_capacity,{int(memory_bytes)}\n")
                f.write(f"memory_usage,{int(memory_usage_bytes)}\n")
        except Exception:
            logging.exception("Failed to write host configuration CSV")

    def write_containers_configuration_csv(self):
        try:
            docker_map = self.get_docker_containers_map()
            wanted = set(self.configuration["cadvisor_containers"].split())
            file_path = os.path.join(self.output_path, "cadvisor_container_configuration.csv")
            with open(file_path, "w") as f:
                f.write("container,key,value\n")
                for entry in docker_map.values():
                    aliases = entry.get("aliases") or []
                    if aliases:
                        raw_name = aliases[0]
                    else:
                        raw_name = (entry.get("name") or "").split("/")[-1]
                    service_name = self.normalize_service_name(raw_name)
                    if ("all" in wanted) or (service_name in wanted):
                        if f"!{service_name}" in wanted:
                            continue
                        spec = entry.get("spec", {})
                        image_value = spec.get("image") or entry.get("image") or ""
                        container_id_value = entry.get("id") or entry.get("container") or ""
                        cpu_section = spec.get("cpu") or {}
                        memory_section = spec.get("memory") or {}
                        cpu_shares_value = (
                            (cpu_section.get("limit") or {}).get("shares")
                            if isinstance(cpu_section.get("limit"), dict)
                            else cpu_section.get("shares")
                        )
                        cpu_quota_value = (
                            (cpu_section.get("limit") or {}).get("quota")
                            if isinstance(cpu_section.get("limit"), dict)
                            else cpu_section.get("quota")
                        )
                        cpu_period_value = (
                            (cpu_section.get("limit") or {}).get("period")
                            if isinstance(cpu_section.get("limit"), dict)
                            else cpu_section.get("period")
                        )
                        memory_limit_value = memory_section.get("limit") or spec.get("memory_limit")
                        created_value = spec.get("creation_time") or entry.get("creation_time") or entry.get("created")
                        labels_value = spec.get("labels") or entry.get("labels")
                        def write_kv(key, value):
                            if value is None:
                                return
                            if isinstance(value, dict):
                                for k, v in value.items():
                                    f.write(f"{service_name},{key}.{k},{v}\n")
                            else:
                                f.write(f"{service_name},{key},{value}\n")
                        write_kv("image", image_value)
                        write_kv("container_id", container_id_value)
                        write_kv("cpu_shares", cpu_shares_value)
                        write_kv("cpu_quota", cpu_quota_value)
                        write_kv("cpu_period", cpu_period_value)
                        write_kv("memory_limit", memory_limit_value)
                        write_kv("created", created_value)
                        write_kv("labels", labels_value)
        except Exception:
            logging.exception("Failed to write containers configuration CSV")

    # ---------------------- lifecycle ----------------------

    def start(self):
        self.writer_thread = threading.Thread(target=self.container_queue_writer, daemon=True)
        self.host_writer_thread = threading.Thread(target=self.host_queue_writer, daemon=True)
        self.worker_thread = threading.Thread(target=self.scheduler_worker, daemon=True)
        self.write_host_configuration_csv()
        self.write_containers_configuration_csv()
        self.writer_thread.start()
        self.worker_thread.start()
        self.host_writer_thread.start()

    def stop(self):
        self.stop_event.set()
        try:
            self.write_queue.put("")
        except Exception:
            pass
        try:
            self.host_write_queue.put("")
        except Exception:
            pass


def before(current_configuration, design_path, output, test_id):
    global _collector_instance
    _collector_instance = CAdvisorCollector(current_configuration, output, test_id)
    _collector_instance.start()


def after(current_configuration, design_path, output, test_id):
    global _collector_instance
    if _collector_instance is not None:
        _collector_instance.stop()
        _collector_instance = None
