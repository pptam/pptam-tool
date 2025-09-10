import logging
import docker
import os
import sched
import threading
from queue import Queue, Empty
from datetime import datetime
import dateutil.parser

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

    def create_docker_client(self, base_address):
        address = base_address.strip()
        if not (address.startswith("tcp://") or address.startswith("http://") or address.startswith("https://")):
            address = f"tcp://{address}"
        if ":" not in address.split("//", 1)[-1]:
            address = f"{address}:2375"
        return docker.DockerClient(base_url=address)

    def calculate_cpu_percent(self, stats):
        try:
            cpu_total = float(stats.get("cpu_stats", {}).get("cpu_usage", {}).get("total_usage", 0.0))
            cpu_total_prev = float(stats.get("precpu_stats", {}).get("cpu_usage", {}).get("total_usage", 0.0))
            system_total = float(stats.get("cpu_stats", {}).get("system_cpu_usage", 0.0))
            system_total_prev = float(stats.get("precpu_stats", {}).get("system_cpu_usage", 0.0))
            cpu_delta = cpu_total - cpu_total_prev
            system_delta = system_total - system_total_prev
            if system_delta <= 0.0:
                return 0.0
            return cpu_delta / system_delta * 100.0
        except Exception:
            logging.exception("Failed to calculate CPU percent")
            return 0.0

    def collect_single_container(self, service_name, container, collection_timestamp):
        try:
            stats = container.stats(stream=False)
            if not stats:
                return
            read_iso = stats.get("read")
            if not read_iso:
                return
            read_dt = dateutil.parser.isoparse(read_iso)
            read_ts = datetime.timestamp(read_dt)
            cpu_percent = self.calculate_cpu_percent(stats)
            mem_usage = int(stats.get("memory_stats", {}).get("usage", 0))
            mem_limit = int(stats.get("memory_stats", {}).get("limit", 0))
            mem_percent = (mem_usage / mem_limit * 100.0) if mem_limit > 0 else 0.0
            a = f"{cpu_percent:.2f}"
            b = f"{mem_percent:.2f}"
            c = f"{float(mem_usage):.2f}"
            d = f"{float(mem_limit):.2f}"
            self.write_queue.put(f"{collection_timestamp},{read_ts},{service_name},{a},{b},{c},{d}\n")
        except Exception:
            logging.exception("Failed to collect stats for container")

    def collect_batch(self):
        if self.stop_event.is_set():
            return
        try:
            collection_timestamp = datetime.timestamp(datetime.utcnow())
            containers_to_watch = self.configuration["docker_stats_containers"].split()
            docker_host = self.configuration["docker_stats_hostname"]
            docker_client = self.create_docker_client(docker_host)
            for container in docker_client.containers.list():
                service_name = container.name
                expected_prefix = f"{self.test_identifier}_"
                if service_name.startswith(expected_prefix):
                    service_name = service_name[len(expected_prefix):]
                first_dot = service_name.find(".")
                if first_dot > 0:
                    service_name = service_name[:first_dot]
                if ("all" in containers_to_watch) or (service_name in containers_to_watch):
                    if f"!{service_name}" in containers_to_watch:
                        continue
                    threading.Thread(target=self.collect_single_container, args=(service_name, container, collection_timestamp), daemon=True).start()
        except Exception:
            logging.exception("Failed to collect batch stats")

    def scheduler_worker(self):
        logging.info("Collecting Docker stats in background.")
        interval_seconds = int(self.configuration["docker_stats_run_every_number_of_seconds"])
        run_time_seconds = int(self.configuration["run_time_in_seconds"])
        number_of_calls = 1 + (run_time_seconds // interval_seconds)
        logging.info(f"Scheduling Docker stats for #{number_of_calls} times.")
        scheduler = sched.scheduler()
        for i in range(number_of_calls):
            if self.stop_event.is_set():
                break
            logging.info(f"Scheduling Docker stats after #{i * interval_seconds} seconds.")
            scheduler.enter(i * interval_seconds, 1, self.collect_batch)
        if not self.stop_event.is_set():
            scheduler.run()

    def queue_writer(self):
        logging.info("Waiting for Docker stats results.")
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
