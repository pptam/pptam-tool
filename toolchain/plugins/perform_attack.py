
#!/usr/bin/env python3
import threading

_executor_instance = None


class AttackExecutor:
    def __init__(self):
        self.stop_event = threading.Event()
        self.worker_thread = None

    def worker(self):
        if not self.stop_event.wait(10):
            print("ATTACK")

    def start(self):
        self.worker_thread = threading.Thread(target=self.worker, daemon=True)
        self.worker_thread.start()

    def stop(self):
        self.stop_event.set()
        if self.worker_thread is not None:
            self.worker_thread.join(timeout=1)


def before(current_configuration, design_path, output, test_id):
    global _executor_instance
    _executor_instance = AttackExecutor()
    _executor_instance.start()


def after(current_configuration, design_path, output, test_id):
    global _executor_instance
    if _executor_instance is not None:
        _executor_instance.stop()
        _executor_instance = None
