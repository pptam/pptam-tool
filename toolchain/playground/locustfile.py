import random
import json
import datetime
import secrets
from locust import HttpUser, task, between, events
import requests
import locust.stats
from datetime import datetime

# @events.spawning_complete.add_listener
# def on_spawning_complete(user_count, **kwargs):
#     print(f"Done: {user_count}")

class TrainTicketUser(HttpUser):

    @task
    def see_offers(self):
        tm = datetime.now()
        tm = datetime(tm.year, tm.month, tm.day, tm.hour, tm.minute, 0 if tm.second < 30 else 30, 0)
        self.client.get("/", verify=False, name = f"/;{int(tm.timestamp())}")


