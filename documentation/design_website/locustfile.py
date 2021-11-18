import random
import json
import datetime
import secrets
from locust import HttpUser, task, between
import requests

class TrainTicketUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def see_offers(self):
        self.client.get("/en", verify=False)
        self.client.get("/en/offers/all", verify=False)
        self.client.get("/en/offer/26", verify=False)
        self.client.get("/en/offer/2", verify=False)
        self.client.get("/en/offer/3", verify=False)


