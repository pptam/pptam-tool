import random
import json
import datetime
import secrets
from locust import HttpUser, task, between
import requests

class JsonUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def see_offers(self):
        self.client.get("/posts", verify=False)
        self.client.get("/posts/1", verify=False)
        self.client.get("/posts/2", verify=False)
        self.client.get("/posts/3", verify=False)
        self.client.get("/comments", verify=False)
        self.client.get("/comments/1", verify=False)
        self.client.get("/comments/2", verify=False)
        self.client.get("/comments/3", verify=False)