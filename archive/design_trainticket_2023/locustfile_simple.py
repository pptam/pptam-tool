from locust import HttpUser, task, between, constant, events
from requests.adapters import HTTPAdapter
from datetime import datetime, timedelta, date
from random import randint
import numpy as np
import logging
import sys
import time
import logging
import uuid
import json
import locust.stats
import time

locust.stats.PERCENTILES_TO_REPORT = [0.25, 0.50, 0.75, 0.80, 0.90, 0.95, 0.98, 0.99, 0.999, 0.9999, 1.0]

def get_json_from_response(response):
    response_as_text = response.content.decode('UTF-8')
    response_as_json = json.loads(response_as_text)
    return response_as_json

def login(client):
    while True:
        try:
            logging.debug(f"Logging in.")
            body = {"username": "fdse_microservice", "password": "111111"}
            response = client.post(url="/api/v1/users/login", json=body, name=get_name_suffix("login"))
            response_as_json = get_json_from_response(response)

            if response_as_json["status"] == 1:
                data = response_as_json["data"]
                user_id = data["userId"]
                token = data["token"]
                return user_id, token
        except:
            pass

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

def get_name_suffix(name):
    return name
        
def home(client):
    client.get("/index.html", name=get_name_suffix("home"))

def get_trip_information(client, from_station, to_station):
    # we always start next Monday
    tomorrow = datetime.now() + timedelta(1)
    next_monday = next_weekday(tomorrow, 0)
    departure_date = next_monday.strftime("%Y-%m-%d")

    while True:
        try:
            logging.debug(f"Getting trip information...")
            body = {"startingPlace": from_station, "endPlace": to_station, "departureTime": departure_date}
            response = client.post(url="/api/v1/travelservice/trips/left", json=body, catch_response=True, name=get_name_suffix("get_trip_information"))
            response_as_json = get_json_from_response(response)

            if response_as_json["status"] == 1:
                break
        except:
            pass

def search_departure(client):
    get_trip_information(client, "Shang Hai", "Su Zhou")

def search_return(client):
    get_trip_information(client, "Su Zhou", "Shang Hai")

def book(client, user_id):
    # we always start next Monday
    tomorrow = datetime.now() + timedelta(1)
    next_monday = next_weekday(tomorrow, 0)
    departure_date = next_monday.strftime("%Y-%m-%d")

    while True:
        try:
            logging.debug(f"Getting insurance types...")
            response = client.get(url="/api/v1/assuranceservice/assurances/types", name=get_name_suffix("book-get_assurance_types"))
            response_as_json = get_json_from_response(response)

            if response_as_json["status"] == 1:
                break
        except:
            pass

    while True:
        try:
            logging.debug(f"Getting food types...")
            response = client.get(url="/api/v1/foodservice/foods/" + departure_date + "/Shang%20Hai/Su%20Zhou/D1345", name=get_name_suffix("book-get_foods"))
            response_as_json = get_json_from_response(response)

            if response_as_json["status"] == 1:
                break
        except:
            pass
    
    while True:
        try:
            logging.debug(f"Getting contacts...")
            response = client.get(url="/api/v1/contactservice/contacts/account/" + user_id, name=get_name_suffix("book-query_contacts"))
            response_as_json = get_json_from_response(response)

            if response_as_json["status"] == 1:
                data = response_as_json["data"]
                contact_id = data[0]["id"] 
                break
        except:
            pass
    
    while True:
        try:
            logging.debug(f"Reserving ticket...")
            body = {"accountId": user_id, "contactsId": contact_id, "tripId": "D1345", "seatType": "2", "date": departure_date, "from": "Shang Hai", "to": "Su Zhou", "assurance": "0", "foodType": 1, "foodName": "Bone Soup", "foodPrice": 2.5, "stationName": "", "storeName": ""}
            response = client.post(url="/api/v1/preserveservice/preserve", json=body, catch_response=True, name=get_name_suffix("book-preserve_ticket"))
            response_as_json = get_json_from_response(response)

            if response_as_json["status"] == 1:
                break
        except:
            pass

def pay(client, user_id):
    while True:
        try:
            body = {"loginId": user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false", "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null", "boughtDateStart": "null", "boughtDateEnd": "null"}
            response = client.post(url="/api/v1/orderservice/order/refresh", json=body, name=get_name_suffix("pay-get_order_information"))
            response_as_json = get_json_from_response(response)

            if response_as_json["status"] == 1:
                data = response_as_json["data"]
                order_id = data[0]["id"]
                break
        except:
            pass
    
    while True:
        try:
            body = {"orderId": order_id, "tripId": "D1345"}
            response = client.post(url="/api/v1/inside_pay_service/inside_payment", json=body, name=self.get_name_suffix("book-pay_order"))
            response_as_json = get_json_from_response(response)

            if response_as_json["status"] == 1:
                break
        except:
            pass
    
        
    

class Requests:
    def __init__(self, client):
        self.client = client
        self.request_id = str(uuid.uuid4())

    def cancel_last_order_with_no_refund(self):
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        self.client.get(url="/api/v1/cancelservice/cancel/" + self.order_id + "/" + self.user_id, headers=head, name=self.get_name_suffix("cancel_ticket"))

    def get_voucher(self):
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        self.client.post(url="/getVoucher", headers=head, json={"orderId": self.order_id, "type": 1}, name=self.get_name_suffix("get_voucher"))

    def consign_ticket(self):
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name
        self.client.get(url="/api/v1/consignservice/consigns/order/" + self.order_id, headers=head, name=self.get_name_suffix("consign_ticket-query"))
        self.client.put(url="/api/v1/consignservice/consigns", name=self.get_name_suffix("consign_ticket-create_consign"), json={"accountId": self.user_id, "handleDate": self.departure_date, "from": "Shang Hai", "to": "Su Zhou", "orderId": self.order_id, "consignee": self.order_id, "phone": "123", "weight": "1", "id": "", "isWithin": "false"}, headers=head)



class MyHttpUser(HttpUser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
        self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

class UserNoLogin(HttpUser):

    def on_start(self):
        self.client.headers.update({"Content-Type": "application/json"})    
        self.client.headers.update({"Accept": "application/json"})    

    @task
    def perfom_task(self):
        logging.debug(f"""Running user "no login" with id {requests.request_id}...""")

        home(self.client)
        search_departure(self.client)
        search_return(self.client)

class UserBooking(HttpUser):

    def on_start(self):
        user_id, token = login(self.client)
        self.client.headers.update({"Authorization": f"Bearer {token}"})
        self.client.headers.update({"Content-Type": "application/json"})    
        self.client.headers.update({"Accept": "application/json"})  
        self.user_id = user_id

    @task
    def perform_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "booking" with id {requests.request_id}...""")

        home(self.client)
        search_departure(self.client)
        search_return(self.client)
        book(self.client, self.user_id)
        pay(self.client, self.user_id)
        

class UserConsignTicket(HttpUser):

    def on_start(self):
        user_id, token = login(self.client)
        self.client.headers.update({"Authorization": f"Bearer {token}"})
        self.client.headers.update({"Content-Type": "application/json"})   
        self.client.headers.update({"Accept": "application/json"})   

    @task
    def perform_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "consign ticket" with id {requests.request_id}...""")

        requests.perform_task("home")
        requests.perform_task("search_departure")
        requests.perform_task("book")
        requests.perform_task("consign_ticket")
        
class UserCancelNoRefund(HttpUser):

    def on_start(self):
        user_id, token = login(self.client)
        self.client.headers.update({"Authorization": f"Bearer {token}"})
        self.client.headers.update({"Content-Type": "application/json"})    
        self.client.headers.update({"Accept": "application/json"})   

    @task
    def perform_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "cancel no refund" with id {requests.request_id}...""")

        requests.perform_task("home")
        requests.perform_task("search_departure")
        requests.perform_task("book")
        requests.perform_task("cancel_last_order_with_no_refund")

class UserRefundVoucher(HttpUser):

    def on_start(self):
        user_id, token = login(self.client)
        self.client.headers.update({"Authorization": f"Bearer {token}"})
        self.client.headers.update({"Content-Type": "application/json"})    
        self.client.headers.update({"Accept": "application/json"})   

    @task
    def perform_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "refound voucher" with id {requests.request_id}...""")

        requests.perform_task("home")
        requests.perform_task("search_departure")
        requests.perform_task("book")
        requests.perform_task("get_voucher")
