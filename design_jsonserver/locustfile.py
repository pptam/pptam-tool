import random
import json
import datetime
import secrets
from locust import HttpUser, task, between
import requests

class JsonUser(HttpUser):
    wait_time = between(5, 9)

    def setup(self):
        self.client.post("/cars", {'name':'great car 1', 'type':'1', 'year':'2001'}, verify=False)
        self.client.post("/cars", {'name':'great car 2', 'type':'2', 'year':'2011'}, verify=False)
        self.client.post("/cars", {'name':'great car 3', 'type':'3', 'year':'2021'}, verify=False)

    @task
    def see_offers(self):
        self.client.get("/cars", verify=False)
        self.client.get("/cars/1", verify=False)
        self.client.get("/cars/2", verify=False)
        self.client.get("/cars/3", verify=False)
