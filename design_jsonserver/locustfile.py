import random
import json
import datetime
import secrets
from locust import HttpUser, task, between, events
import requests

@events.test_start.add_listener
def setup(environment, **kwargs):
    headers = {'content-type': 'application/json'}

    for i in range(10):
        name_of_car = "Great car {i}"
        type_of_car = random.randrange(1, 10)
        year_of_car = random.randrange(1920, 2021)
        requests.post(f"{environment.host}/cars", data=json.dumps({'name': name_of_car, 'type': type_of_car, 'year': year_of_car}), headers=headers, verify=False)
        
class JsonUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def see_all(self):
        headers = {'content-type': 'application/json'}
        self.client.get("/cars", headers=headers, verify=False)
        
    @task
    def see_cars(self):
        headers = {'content-type': 'application/json'}
        for _ in range(random.randrange(1, 20)):
            car = random.randrange(1, 10)
            self.client.get(f"/cars/{car}", headers=headers, verify=False)