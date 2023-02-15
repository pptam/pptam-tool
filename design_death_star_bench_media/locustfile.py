import random
import json
import datetime
import secrets
from locust import HttpUser, task, between, events
import requests

class MediaUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def see_all(self):
        headers = {'content-type': 'application/json'}
        self.client.get("/", headers=headers, verify=False)
        