#!/usr/bin/env python
import threading
import time


def get_docker_stats(docker_client):
    print("start")
    time.sleep(2)
    print("stop")


if __name__ == "__main__":
    print("!")
    docker_client = "abc"
    run_docker_stats_in_background = threading.Thread(target=get_docker_stats, args=(docker_client,), daemon=False)
    run_docker_stats_in_background.start()