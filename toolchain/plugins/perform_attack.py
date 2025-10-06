
#!/usr/bin/env python3
import threading
import time
import random
import logging
import importlib
import math

_executor_instance = None


class AttackExecutor:
    def __init__(self, configuration, design_path, output_path, test_identifier):
        self.configuration = configuration
        self.design_path = design_path
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.stop_event = threading.Event()
        self.worker_thread = None

    def _resolve_attack(self):
        name = (self.configuration.get("attack_name") or "").strip()
        if not name:
            logging.info("perform_attack: ATTACK_NAME not set; no attack will run.")
            return None, None

        module_name = f"attacks.{name}"
        try:
            module = importlib.import_module(module_name)
        except Exception as e:
            logging.error(f"perform_attack: Cannot import attack module '{module_name}': {repr(e)}")
            return None, None

        attack_class = getattr(module, "Attack", None)
        attack_func = getattr(module, "run", None) if attack_class is None else None
        if attack_class is None and attack_func is None:
            logging.error(
                f"perform_attack: Attack '{name}' must expose class 'Attack' or function 'run'.")
            return None, None

        return attack_class, attack_func

    def _compute_schedule(self):
        # Total active run time (seconds) of the performance test
        total_run_time = int(float(self.configuration.get("run_time_in_seconds", 0)))
        if total_run_time <= 0:
            return None

        # Delay before run phase starts (from 'before' to 'run')
        delay_before_run = int(float(self.configuration.get("seconds_to_wait_before_run", 0)))

        # Attack duration: ATTACK_LENGTH_RATIO of total run time (no default; random if unset)
        raw_ratio = self.configuration.get("attack_length_ratio")
        if raw_ratio is None or str(raw_ratio).strip() == "":
            ratio = random.random()
            logging.info(f"perform_attack: ATTACK_LENGTH_RATIO not set; using random ratio {ratio:.3f}.")
        else:
            try:
                ratio = float(raw_ratio)
            except Exception:
                ratio = random.random()
                logging.info(f"perform_attack: invalid ATTACK_LENGTH_RATIO; using random ratio {ratio:.3f}.")
        # clamp to [0,1]
        ratio = max(0.0, min(1.0, ratio))

        duration = total_run_time * ratio

        # Start policy
        start_type = (self.configuration.get("attack_start_time_type") or "random").strip().lower()

        if start_type == "none":
            start_offset_within_run = total_run_time * ratio
            # Ensure we finish within the run window
            if start_offset_within_run + duration > total_run_time:
                start_offset_within_run = max(0.0, total_run_time - duration)
        else:
            # random start within [0, RUN - duration]
            earliest_offset = 0.0
            latest_offset = max(0.0, total_run_time - duration)
            start_offset_within_run = random.uniform(earliest_offset, latest_offset)

        # Absolute delay from now (we are in 'before' phase)
        start_after_seconds = delay_before_run + start_offset_within_run

        return max(0.0, start_after_seconds), max(0.1, duration)

    def _run_attack(self, attack_class, attack_func, duration_seconds):
        try:
            if attack_class is not None:
                # Expected interface: Attack(configuration, design_path, output_path, test_identifier)
                instance = attack_class(self.configuration, self.design_path, self.output_path, self.test_identifier)
                vector_label = getattr(instance, "VECTOR_NAME", getattr(instance, "vector_name", attack_class.__name__))
                target_service = getattr(instance, "TARGET_SERVICE", getattr(instance, "target_service", None))
                resource_hint = getattr(instance, "RESOURCE_DIMENSIONS", None)
                meta_suffix = ""
                if target_service:
                    meta_suffix += f" target_service={target_service}"
                if resource_hint:
                    meta_suffix += f" focus={','.join(resource_hint)}"
                logging.info("perform_attack: activating vector '%s'%s.", vector_label, meta_suffix)
                # Expected method: run(duration_seconds, stop_event)
                instance.run(duration_seconds, self.stop_event)
            else:
                # Expected function signature: run(duration_seconds, stop_event, configuration, design_path, output_path, test_identifier)
                attack_func(duration_seconds, self.stop_event, self.configuration, self.design_path, self.output_path, self.test_identifier)
        except Exception:
            logging.exception("perform_attack: Attack raised an exception.")

    def worker(self):
        attack_class, attack_func = self._resolve_attack()
        if attack_class is None and attack_func is None:
            return

        schedule = self._compute_schedule()
        if schedule is None:
            logging.warning("perform_attack: RUN_TIME_IN_SECONDS not set or invalid; skipping attack.")
            return

        start_after_seconds, duration_seconds = schedule
        logging.info(
            f"perform_attack: Scheduled attack to start in {start_after_seconds:.2f}s"
            f" for duration {duration_seconds:.2f}s (test_id={self.test_identifier}).")

        # Wait until the scheduled start or until stopped
        if self.stop_event.wait(timeout=start_after_seconds):
            return

        start_ts = time.time()
        logging.info("perform_attack: Starting attack now.")
        self._run_attack(attack_class, attack_func, duration_seconds)

        # Ensure we don't overrun if the attack implementation returned early; keep up to duration if needed
        elapsed = time.time() - start_ts
        remaining = duration_seconds - elapsed
        if remaining > 0:
            self.stop_event.wait(timeout=remaining)
        logging.info("perform_attack: Attack window finished.")

    def start(self):
        self.worker_thread = threading.Thread(target=self.worker, daemon=True)
        self.worker_thread.start()

    def stop(self):
        self.stop_event.set()
        if self.worker_thread is not None:
            # Give a short time to finish gracefully
            self.worker_thread.join(timeout=2)


def before(current_configuration, design_path, output, test_id):
    global _executor_instance
    _executor_instance = AttackExecutor(current_configuration, design_path, output, test_id)
    _executor_instance.start()


def after(current_configuration, design_path, output, test_id):
    global _executor_instance
    if _executor_instance is not None:
        _executor_instance.stop()
        _executor_instance = None
