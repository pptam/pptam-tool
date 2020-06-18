import random
import json
import datetime
import secrets
# from locust import HttpUser, task, between
import requests

session = requests.Session()
session.headers.update({'Accept': 'application/json'})
session.headers.update({'Content-Type': 'application/json'})
response1 = session.get('http://10.7.20.113:8080/index.html')

response = session.post(
    "http://10.7.20.113:8080/api/v1/users/login",
    '{"username": "fdse_microservice", "password": "111111"}')
response_as_json = json.loads(response.content)["data"]
token = response_as_json["token"]
bearer = "Bearer " + token
session.headers.update({"Authorization": bearer})

user_id = response_as_json["userId"]

trip_start = "Shang Hai"
trip_end = "Su Zhou"
trip_date = "2020-06-18T08:00:00.000"

data = '{"departureTime":"' + trip_date + '","endPlace":"' + trip_end + '","startingPlace":"' + trip_start + '"}'
req = session.post('http://10.7.20.113:8080/api/v1/travelservice/trips/left',
                   data)
print(req.content)


