#!/usr/bin/env python3.7
import docker

client = docker.DockerClient(base_url='10.7.20.69:2375')
for container in client.containers.list():
    print(container.stats(stream=False))
