import logging
import os
import sched
import threading
from queue import Queue, Empty
from datetime import datetime
import dateutil.parser
import requests

_collector_instance = None


class DockerStatsCollector:
    def __init__(self, configuration, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.stop_event = threading.Event()
        self.write_queue = Queue()
        self.writer_thread = None
        self.worker_thread = None

    def get_cadvisor_base_url(self):
        host_value = self.configuration.get("DOCKER_STATS_HOSTNAME") or self.configuration.get("docker_stats_hostname")
        if not host_value:
            raise ValueError("DOCKER_STATS_HOSTNAME not configured")
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
            mem_percent = (mem_usage / mem_limit * 100.0) if mem_limit > 0 else 0.0
            a = f"{cpu_percent:.2f}"
            b = f"{mem_percent:.2f}"
            c = f"{float(mem_usage):.2f}"
            d = f"{float(mem_limit):.2f}"
            self.write_queue.put(f"{collection_timestamp},{datetime.timestamp(dateutil.parser.isoparse(current_sample.get('timestamp')))},{service_name},{a},{b},{c},{d}\n")
        except Exception:
            logging.exception("Failed to collect cAdvisor stats for container")

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
        wanted = set(self.configuration["docker_stats_containers"].split())
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

    def collect_batch_via_cadvisor(self):
        if self.stop_event.is_set():
            return
        try:
            collection_timestamp = datetime.timestamp(datetime.utcnow())
            containers = self.list_cadvisor_containers()
            for service_name, entry in self.match_containers_to_watch(containers):
                threading.Thread(target=self.collect_single_container_from_cadvisor, args=(service_name, entry, collection_timestamp), daemon=True).start()
        except Exception:
            logging.exception("Failed to collect batch via cAdvisor")

    def scheduler_worker(self):
        logging.info("Collecting container stats in background via cAdvisor.")
        interval_seconds = int(self.configuration["docker_stats_run_every_number_of_seconds"])
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

    def queue_writer(self):
        logging.info("Waiting for container stats results.")
        file_path = os.path.join(self.output_path, "docker_stats.csv")
        with open(file_path, "w") as f:
            f.write("collected,timestamp,service,cpu_usage_percent,memory_usage_percent,memory_usage,memory_limit\n")
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

    def start(self):
        self.writer_thread = threading.Thread(target=self.queue_writer, daemon=True)
        self.worker_thread = threading.Thread(target=self.scheduler_worker, daemon=True)
        self.writer_thread.start()
        self.worker_thread.start()

    def stop(self):
        self.stop_event.set()
        try:
            self.write_queue.put("")
        except Exception:
            pass


def before(current_configuration, design_path, output, test_id):
    global _collector_instance
    _collector_instance = DockerStatsCollector(current_configuration, output, test_id)
    _collector_instance.start()


def after(current_configuration, design_path, output, test_id):
    global _collector_instance
    if _collector_instance is not None:
        _collector_instance.stop()
        _collector_instance = None
