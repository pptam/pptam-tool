import random
import json
import datetime
import secrets
from locust import HttpUser, task, between
import requests


class TrainTicketUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def search(self):
        print("----- search")
        self.client.get("/index.html")

        trip_start = "Shang Hai"
        trip_end = "Su Zhou"
        trip_date = "2020-06-18T08:00:00.000"
        data = {
            "departureTime": trip_date,
            "endPlace": trip_end,
            "startingPlace": trip_start
        }

        self.client.post(url="/api/v1/travelservice/trips/left",
                         json=data,
                         headers={
                             "Authorization": self.bearer,
                             "Accept": "application/json",
                             "Content-Type": "application/json"
                         },
                         name="Search")

    def on_start(self):
        print("----- on_start")

        # Removes trailing / from the host name to avoid exceptions in the tests
        self.host = self.host.rstrip("/")

        response = self.client.post(url="/api/v1/users/login",
                                    json={
                                        "username": "fdse_microservice",
                                        "password": "111111"
                                    })

        response_as_json = json.loads(response.content)["data"]
        token = response_as_json["token"]
        self.bearer = "Bearer " + token
        self.user_id = response_as_json["userId"]

