import logging
import os
import sched
import threading
from queue import Queue, Empty
from datetime import datetime
import requests
import re

_collector_instance = None

class ScaphandreCollector:
    def __init__(self, configuration, output_path, test_identifier):
        self.configuration = configuration
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.stop_event = threading.Event()
        self.write_queue = Queue()
        self.writer_thread = None
        self.worker_thread = None

    def get_scaphandre_base_url(self):
        host_value = self.configuration.get("scaphandre_hostname")
        if not host_value:
            raise ValueError("SCAPHANDRE_HOSTNAME not configured")
        if host_value.startswith("http://") or host_value.startswith("https://"):
            base = host_value
        else:
            base = f"http://{host_value}"
        if ":" not in base.split("//", 1)[-1]:
            base = f"{base}:8080"
        return base.rstrip("/")

    def fetch_prometheus_metrics(self):
        url = f"{self.get_scaphandre_base_url()}/metrics"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.splitlines()

    def parse_prometheus_line(self, line):
        """
        Parse a Prometheus metric line like:
        scaph_process_memory_bytes{pid="17378",exe="/usr/local/bin/scaphandre",cmdline="..."} 23547904
        
        Returns: (metric_name, labels_dict, value)
        """
        # Skip comments and empty lines
        if line.startswith("#") or not line.strip():
            return None, None, None
            
        # Regular expression to parse Prometheus format
        # Matches: metric_name{label1="value1",label2="value2"} value
        pattern = r'^([a-zA-Z_:][a-zA-Z0-9_:]*)\{([^}]*)\}\s+(.+)$'
        match = re.match(pattern, line)
        
        if not match:
            # Try to match metric without labels: metric_name value
            simple_pattern = r'^([a-zA-Z_:][a-zA-Z0-9_:]*)\s+(.+)$'
            simple_match = re.match(simple_pattern, line)
            if simple_match:
                metric_name = simple_match.group(1)
                value = simple_match.group(2)
                return metric_name, {}, float(value)
            return None, None, None
        
        metric_name = match.group(1)
        labels_str = match.group(2)
        value = match.group(3)
        
        # Parse labels
        labels = {}
        if labels_str:
            # Split labels by comma, but be careful with quoted values
            label_pattern = r'([a-zA-Z_][a-zA-Z0-9_]*)="([^"]*)"'
            for label_match in re.finditer(label_pattern, labels_str):
                key = label_match.group(1)
                val = label_match.group(2)
                labels[key] = val
        
        try:
            return metric_name, labels, float(value)
        except ValueError:
            return None, None, None

    def parse_metrics(self, lines):
        metrics = {}
        for line in lines:
            try:
                metric_name, labels, value = self.parse_prometheus_line(line)
                if metric_name is None or 'pid' not in labels:
                    continue
                    
                pid = labels['pid']
                if pid not in metrics:
                    metrics[pid] = {}
                
                # Map Scaphandre metric names to our expected format
                if metric_name == "scaph_process_memory_bytes":
                    metrics[pid]["memory_bytes"] = value
                elif metric_name == "scaph_process_disk_total_read_bytes":
                    # Use total read bytes as disk_bytes (or you might want read + write)
                    metrics[pid]["disk_bytes"] = value
                elif metric_name == "scaph_process_disk_total_write_bytes":
                    # Add write bytes to existing disk_bytes
                    current_disk = metrics[pid].get("disk_bytes", 0.0)
                    metrics[pid]["disk_bytes"] = current_disk + value
                elif metric_name == "scaph_process_cpu_usage_percentage":
                    # Convert percentage to seconds (this might need adjustment based on your needs)
                    # You might want to accumulate this over time or use a different approach
                    metrics[pid]["cpu_seconds"] = value / 100.0  # Convert percentage to fraction
                elif metric_name == "scaph_process_power_consumption_microwatts":
                    metrics[pid]["consumption_milliwatts"] = value / 1000.0  # Convert to watts
                    
            except Exception as e:
                logging.warning(f"Failed to parse line: {line}, error: {e}")
                continue
        return metrics

    def collect_batch(self):
        if self.stop_event.is_set():
            return
        try:
            collection_timestamp = round(datetime.timestamp(datetime.utcnow()))
            metrics = self.parse_metrics(self.fetch_prometheus_metrics())
            for pid, vals in metrics.items():
                cpu_seconds = vals.get("cpu_seconds", 0.0)
                mem_bytes = vals.get("memory_bytes", 0.0)
                disk_bytes = vals.get("disk_bytes", 0.0)
                consumption_milliwatts = vals.get("consumption_milliwatts", 0.0)
                self.write_queue.put(
                    f"{collection_timestamp},{pid},{cpu_seconds},{mem_bytes},{disk_bytes},{consumption_milliwatts}\n"
                )
        except Exception:
            logging.exception("Failed to collect batch via Scaphandre")

    def scheduler_worker(self):
        logging.info("Collecting process stats in background via Scaphandre.")
        interval_seconds = int(self.configuration["scaphandre_run_every_number_of_seconds"])
        run_time_seconds = int(self.configuration["run_time_in_seconds"])
        number_of_calls = 1 + (run_time_seconds // interval_seconds)
        scheduler = sched.scheduler()
        for i in range(number_of_calls):
            if self.stop_event.is_set():
                break
            scheduler.enter(i * interval_seconds, 1, self.collect_batch)
        if not self.stop_event.is_set():
            scheduler.run()

    def queue_writer(self):
        logging.info("Waiting for process stats results.")
        file_path = os.path.join(self.output_path, "scaphandre_process.csv")
        with open(file_path, "w") as f:
            f.write("collected,pid,cpu_seconds,memory_bytes,disk_bytes,consumption_milliwatts\n")
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
    _collector_instance = ScaphandreCollector(current_configuration, output, test_id)
    _collector_instance.start()

def after(current_configuration, design_path, output, test_id):
    global _collector_instance
    if _collector_instance is not None:
        _collector_instance.stop()
        _collector_instance = None