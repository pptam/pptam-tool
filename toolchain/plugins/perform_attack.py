
#!/usr/bin/env python3
import threading
import time
import random
import logging
import importlib
from typing import List

_executor_instance = None


class AttackExecutor:
    def __init__(self, configuration, design_path, output_path, test_identifier):
        self.configuration = configuration
        self.design_path = design_path
        self.output_path = output_path
        self.test_identifier = test_identifier
        self.stop_event = threading.Event()
        self.worker_thread = None

    def _resolve_attack(self, name):
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

    def _parse_attack_names_list(self) -> List[str]:
        raw = self.configuration.get("attack_names_list")
        if not raw:
            return []
        tokens = raw.replace(",", " ").split()
        return [token.strip() for token in tokens if token.strip()]

    def _select_attack_names(self) -> List[str]:
        names_list = self._parse_attack_names_list()
        if names_list:
            try:
                attack_count = int(float(self.configuration.get("attack_numbers", 1)))
            except Exception:
                attack_count = 1
            if attack_count <= 0:
                logging.info("perform_attack: ATTACK_NUMBERS <= 0; no attacks selected.")
                return []
            unique_names = list(dict.fromkeys(names_list))
            if attack_count >= len(unique_names):
                selected = unique_names
            else:
                selected = random.sample(unique_names, attack_count)
            logging.info("perform_attack: selected attacks %s from ATTACK_NAMES_LIST=%s (count=%d).",
                         selected, unique_names, attack_count)
            return selected

        name = (self.configuration.get("attack_name") or "").strip()
        if name:
            logging.info("perform_attack: ATTACK_NAME set to '%s'.", name)
            return [name]

        logging.info("perform_attack: no attacks requested (ATTACK_NAME empty and ATTACK_NAMES_LIST empty).")
        return []

    def _compute_timing_parameters(self):
        total_run_time = int(float(self.configuration.get("run_time_in_seconds", 0)))
        if total_run_time <= 0:
            return None

        delay_before_run = float(self.configuration.get("seconds_to_wait_before_run", 0) or 0)

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
        ratio = max(0.0, min(1.0, ratio))

        duration = total_run_time * ratio
        if duration <= 0.0:
            duration = 0.1
        duration = min(duration, total_run_time)
        if duration <= 0.0:
            duration = total_run_time
        duration = max(0.1, duration)
        duration = min(duration, total_run_time)

        start_type = (self.configuration.get("attack_start_time_type") or "random").strip().lower()

        return {
            "total_run_time": float(total_run_time),
            "delay_before_run": max(0.0, delay_before_run),
            "ratio": ratio,
            "duration": duration,
            "start_type": start_type,
        }

    def _schedule_attack(self, timing_params):
        total_run_time = timing_params["total_run_time"]
        delay_before_run = timing_params["delay_before_run"]
        duration = timing_params["duration"]
        ratio = timing_params["ratio"]
        start_type = timing_params["start_type"]

        if duration >= total_run_time:
            start_offset_within_run = 0.0
        elif start_type == "none":
            start_offset_within_run = total_run_time * ratio
            if start_offset_within_run + duration > total_run_time:
                start_offset_within_run = max(0.0, total_run_time - duration)
        else:
            latest_offset = max(0.0, total_run_time - duration)
            start_offset_within_run = random.uniform(0.0, latest_offset)

        start_after_seconds = delay_before_run + start_offset_within_run
        return max(0.0, start_after_seconds), duration

    def _prepare_attack_specs(self):
        selected_names = self._select_attack_names()
        if not selected_names:
            return []

        timing_params = self._compute_timing_parameters()
        if timing_params is None:
            logging.warning("perform_attack: RUN_TIME_IN_SECONDS not set or invalid; skipping attacks.")
            return []

        specs = []
        for name in selected_names:
            attack_class, attack_func = self._resolve_attack(name)
            if attack_class is None and attack_func is None:
                continue
            start_after, duration = self._schedule_attack(timing_params)
            specs.append({
                "name": name,
                "attack_class": attack_class,
                "attack_func": attack_func,
                "start_after": start_after,
                "duration": duration,
            })

        return specs

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
        specs = self._prepare_attack_specs()
        if not specs:
            return

        threads = []

        def attack_thread(spec):
            name = spec["name"]
            start_after = spec["start_after"]
            duration = spec["duration"]
            attack_class = spec["attack_class"]
            attack_func = spec["attack_func"]

            logging.info(
                "perform_attack: vector '%s' scheduled to start in %.2fs for %.2fs.",
                name,
                start_after,
                duration,
            )
            if self.stop_event.wait(timeout=start_after):
                logging.info("perform_attack: vector '%s' cancelled before start.", name)
                return

            start_ts = time.time()
            logging.info("perform_attack: vector '%s' starting now.", name)
            self._run_attack(attack_class, attack_func, duration)

            elapsed = time.time() - start_ts
            remaining = duration - elapsed
            if remaining > 0:
                self.stop_event.wait(timeout=remaining)
            logging.info("perform_attack: vector '%s' window finished.", name)

        for spec in specs:
            t = threading.Thread(target=attack_thread, args=(spec,), daemon=True)
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

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
