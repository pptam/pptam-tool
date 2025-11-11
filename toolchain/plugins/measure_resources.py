#!/usr/bin/env python3
import logging
import os
import re
import sched
import threading
from queue import Queue, Empty
from datetime import datetime
import dateutil.parser
import requests

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
        # Keep a set to avoid duplicate entries when Option A
        self.seen_samples = set()

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

    # ---------------------------------------------------------------------
    # New: Collect container stats directly from /api/v1.3/docker/
    # ---------------------------------------------------------------------
    def collect_batch_via_cadvisor(self):
        if self.stop_event.is_set():
            return
        try:
            collection_timestamp = round(datetime.timestamp(datetime.utcnow()))
            base = self.get_cadvisor_base_url()
            url = f"{base}/api/v1.3/docker/"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            docker_data = response.json()

            for container_id, container_entry in docker_data.items():
                aliases = container_entry.get("aliases") or []
                service_name = aliases[0] if aliases else container_entry.get("name", "").split("/")[-1]
                stats_list = container_entry.get("stats", [])
                image_name = container_entry.get("spec", {}).get("image", "")

                for s in stats_list:
                    ts = s.get("timestamp")
                    if not ts:
                        continue
                    try:
                        sample_ts = round(datetime.timestamp(dateutil.parser.isoparse(ts)))
                    except Exception:
                        continue

                    unique_key = (container_id, sample_ts)
                    if unique_key in self.seen_samples:
                        continue
                    self.seen_samples.add(unique_key)

                    # Extract metrics
                    cpu_total = float(s.get("cpu", {}).get("usage", {}).get("total", 0.0))
                    mem_usage = int(s.get("memory", {}).get("usage", 0))
                    mem_limit = int(s.get("memory", {}).get("limit", 0))

                    # Filesystem I/O
                    reads_count, writes_count, read_bytes, write_bytes = self.extract_filesystem_counters(s)

                    # Network I/O
                    net = s.get("network", {}) or {}
                    rx_bytes = int(net.get("rx_bytes", 0))
                    tx_bytes = int(net.get("tx_bytes", 0))
                    rx_packets = int(net.get("rx_packets", 0))
                    tx_packets = int(net.get("tx_packets", 0))

                    line = (
                        f"{collection_timestamp},{sample_ts},{service_name},{image_name},"
                        f"{cpu_total},{mem_usage},{mem_limit},{reads_count},{writes_count},"
                        f"{read_bytes},{write_bytes},{rx_bytes},{tx_bytes},{rx_packets},{tx_packets}\n"
                    )
                    self.write_queue.put(line)

            # also collect host stats
            threading.Thread(
                target=self.collect_host_from_cadvisor,
                args=(collection_timestamp,),
                daemon=True,
            ).start()

        except Exception:
            logging.exception("Failed to collect batch via cAdvisor (/api/v1.3/docker/)")

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
            wanted = set(self.configuration.get("cadvisor_containers", "all").split())
            file_path = os.path.join(self.output_path, "cadvisor_container_configuration.csv")
            with open(file_path, "w") as f:
                f.write("container,key,value\n")
                for entry in docker_map.values():
                    aliases = entry.get("aliases") or []
                    raw_name = aliases[0] if aliases else (entry.get("name") or "").split("/")[-1]
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



    def extract_filesystem_counters(self, sample):
        filesystem_list = sample.get("filesystem") or sample.get("fs") or []
        total_reads = total_writes = total_read_bytes = total_write_bytes = 0
        for fs_entry in filesystem_list:
            reads_value = fs_entry.get("reads") or fs_entry.get("readsCompleted")
            writes_value = fs_entry.get("writes") or fs_entry.get("writesCompleted")
            read_bytes_value = (
                fs_entry.get("readBytes")
                or fs_entry.get("readbytes")
                or fs_entry.get("read_bytes")
            )
            write_bytes_value = (
                fs_entry.get("writeBytes")
                or fs_entry.get("writebytes")
                or fs_entry.get("write_bytes")
            )
            try:
                total_reads += int(reads_value or 0)
                total_writes += int(writes_value or 0)
                total_read_bytes += int(read_bytes_value or 0)
                total_write_bytes += int(write_bytes_value or 0)
            except Exception:
                continue
        return total_reads, total_writes, total_read_bytes, total_write_bytes

    def collect_host_from_cadvisor(self, collection_timestamp):
        try:
            host_entry = self.get_host_container_stats()
            stats_list = host_entry.get("stats", [])
            if len(stats_list) < 2:
                return
            previous_sample = stats_list[-2]
            current_sample = stats_list[-1]
            cpu_prev = float(previous_sample.get("cpu", {}).get("usage", {}).get("total", 0.0))
            cpu_curr = float(current_sample.get("cpu", {}).get("usage", {}).get("total", 0.0))
            ts_prev = dateutil.parser.isoparse(previous_sample.get("timestamp"))
            ts_curr = dateutil.parser.isoparse(current_sample.get("timestamp"))
            interval_ns = (ts_curr - ts_prev).total_seconds() * 1e9
            cpu_percent = (max(cpu_curr - cpu_prev, 0.0) / interval_ns * 100.0) if interval_ns > 0 else 0.0

            mem_usage = int(current_sample.get("memory", {}).get("usage", 0))
            mem_limit = int(current_sample.get("memory", {}).get("limit", 0))
            reads_count, writes_count, read_bytes, write_bytes = self.extract_filesystem_counters(current_sample)
            host_label = self.get_machine_hostname()
            sample_ts = round(datetime.timestamp(ts_curr))
            self.host_write_queue.put(
                f"{collection_timestamp},{sample_ts},{host_label},{cpu_percent:.2f},{mem_usage},{mem_limit},"
                f"{reads_count},{writes_count},{read_bytes},{write_bytes}\n"
            )
        except Exception:
            logging.exception("Failed to collect host stats")

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

    def get_machine_hostname(self):
        try:
            data = self.get_machine_info()
            return data.get("machineInfo", {}).get("name") or data.get("name") or "host"
        except Exception:
            return "host"

    def get_docker_containers_map(self):
        base = self.get_cadvisor_base_url()
        url = f"{base}/api/v1.3/docker/"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Unexpected cAdvisor docker payload")
        return data

    @staticmethod
    def normalize_service_name(raw_name):
        """
        Normalize docker/container aliases so configuration can match them reliably.
        - Trim whitespace and leading/trailing separators
        - Collapse common docker-compose suffixes like `_1` or `-2`
        - Lowercase and replace problematic chars with `_`
        """
        if not raw_name:
            return "unknown"
        service = str(raw_name).strip()
        if not service:
            return "unknown"
        service = service.strip("/ ")
        # Replace separators that commonly appear in alias names
        service = service.replace(" ", "_").replace(":", "_").replace(".", "_").replace("/", "_")
        # Drop docker-compose replica suffixes (_1, -2, etc.)
        service = re.sub(r"([_-])\d+$", "", service)
        service = service.strip("_-")
        return service.lower() or "unknown"

    def scheduler_worker(self):
        logging.info("Collecting container stats in background via /api/v1.3/docker/.")
        interval_seconds = int(self.configuration["cadvisor_run_every_number_of_seconds"])
        run_time_seconds = int(self.configuration["run_time_in_seconds"])
        number_of_calls = 1 + (run_time_seconds // interval_seconds)
        scheduler = sched.scheduler()
        for i in range(number_of_calls):
            if self.stop_event.is_set():
                break
            scheduler.enter(i * interval_seconds, 1, self.collect_batch_via_cadvisor)
        if not self.stop_event.is_set():
            scheduler.run()

    def container_queue_writer(self):
        logging.info("Waiting for container stats results.")
        file_path = os.path.join(self.output_path, "cadvisor_container.csv")
        with open(file_path, "w") as f:
            f.write(
                "collected,timestamp,service,image,cpu_total,memory_usage,memory_limit,"
                "reads,writes,readBytes,writeBytes,rx_bytes,tx_bytes,rx_packets,tx_packets\n"
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
        logging.info("Waiting for host stats results.")
        file_path = os.path.join(self.output_path, "cadvisor_host.csv")
        with open(file_path, "w") as f:
            f.write("collected,timestamp,host,cpu_usage,memory_usage,memory_limit,reads,writes,readBytes,writeBytes\n")
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

    def start(self):
        self.writer_thread = threading.Thread(target=self.container_queue_writer, daemon=True)
        self.host_writer_thread = threading.Thread(target=self.host_queue_writer, daemon=True)
        self.worker_thread = threading.Thread(target=self.scheduler_worker, daemon=True)
        self.write_host_configuration_csv()          # <-- add
        self.write_containers_configuration_csv()    # <-- add
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
