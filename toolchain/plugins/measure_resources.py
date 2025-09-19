#!/usr/bin/env python3
import logging
import os
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

    def extract_filesystem_counters(self, sample):
        filesystem_list = sample.get("filesystem") or sample.get("fs") or []
        total_reads = 0
        total_writes = 0
        total_read_bytes = 0
        total_write_bytes = 0
        for fs_entry in filesystem_list:
            reads_value = fs_entry.get("reads")
            if reads_value is None:
                reads_value = fs_entry.get("readsCompleted")
            writes_value = fs_entry.get("writes")
            if writes_value is None:
                writes_value = fs_entry.get("writesCompleted")
            read_bytes_value = fs_entry.get("readBytes")
            if read_bytes_value is None:
                read_bytes_value = fs_entry.get("readbytes")
            if read_bytes_value is None:
                read_bytes_value = fs_entry.get("read_bytes")
            write_bytes_value = fs_entry.get("writeBytes")
            if write_bytes_value is None:
                write_bytes_value = fs_entry.get("writebytes")
            if write_bytes_value is None:
                write_bytes_value = fs_entry.get("write_bytes")
            try:
                total_reads += int(reads_value or 0)
                total_writes += int(writes_value or 0)
                total_read_bytes += int(read_bytes_value or 0)
                total_write_bytes += int(write_bytes_value or 0)
            except Exception:
                continue
        return total_reads, total_writes, total_read_bytes, total_write_bytes

    def collect_single_container_from_cadvisor(self, service_name, container_entry, collection_timestamp):
        try:
            stats_list = container_entry.get("stats", [])
            if len(stats_list) < 2:
                return
            previous_sample = stats_list[-2]
            current_sample = stats_list[-1]
            cpu_percent = self.calculate_cpu_percent_from_cadvisor_samples(previous_sample, current_sample)
            mem_usage = int(current_sample.get("memory", {}).get("usage", 0))
            mem_limit = int(current_sample.get("memory", {}).get("limit", 0))
            reads_count, writes_count, read_bytes, write_bytes = self.extract_filesystem_counters(current_sample)
            a = f"{cpu_percent:.2f}"
            c = f"{float(mem_usage):.2f}"
            d = f"{float(mem_limit):.2f}"
            r = str(int(reads_count))
            w = str(int(writes_count))
            rb = str(int(read_bytes))
            wb = str(int(write_bytes))
            col_ts = round(collection_timestamp)
            sample_ts = round(datetime.timestamp(dateutil.parser.isoparse(current_sample.get('timestamp'))))
            self.write_queue.put(f"{col_ts},{sample_ts},{service_name},{a},{c},{d},{r},{w},{rb},{wb}\n")
        except Exception:
            logging.exception("Failed to collect cAdvisor stats for container")

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
            reads_count, writes_count, read_bytes, write_bytes = self.extract_filesystem_counters(current_sample)
            a = f"{cpu_percent:.2f}"
            c = f"{float(mem_usage):.2f}"
            d = f"{float(mem_limit):.2f}"
            r = str(int(reads_count))
            w = str(int(writes_count))
            rb = str(int(read_bytes))
            wb = str(int(write_bytes))
            host_label = self.get_machine_hostname()
            col_ts = round(collection_timestamp)
            sample_ts = round(datetime.timestamp(dateutil.parser.isoparse(current_sample.get('timestamp'))))
            self.host_write_queue.put(f"{col_ts},{sample_ts},{host_label},{a},{c},{d},{r},{w},{rb},{wb}\n")
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

    def collect_batch_via_cadvisor(self):
        if self.stop_event.is_set():
            return
        try:
            collection_timestamp = datetime.timestamp(datetime.utcnow())
            containers = self.list_cadvisor_containers()
            for service_name, entry in self.match_containers_to_watch(containers):
                threading.Thread(target=self.collect_single_container_from_cadvisor, args=(service_name, entry, collection_timestamp), daemon=True).start()
            threading.Thread(target=self.collect_host_from_cadvisor, args=(collection_timestamp,), daemon=True).start()
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

    def container_queue_writer(self):
        logging.info("Waiting for container stats results.")
        file_path = os.path.join(self.output_path, "cadvisor_container.csv")
        with open(file_path, "w") as f:
            f.write("collected,timestamp,service,cpu_usage,memory_usage,memory_limit,reads,writes,readBytes,writeBytes\n")
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
