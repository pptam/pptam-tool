from locust import HttpUser, task, between, constant
from datetime import datetime, timedelta, date
from random import randint
import numpy as np
import logging
import sys
import time
import logging
import uuid
import json
from requests.adapters import HTTPAdapter
import locust.stats

locust.stats.PERCENTILES_TO_REPORT = [0.25, 0.50, 0.75, 0.80, 0.90, 0.95, 0.98, 0.99, 0.999, 0.9999, 1.0]

LOG_STATISTICS_IN_HALF_MINUTE_CHUNKS = (${LOG_STATISTICS_IN_HALF_MINUTE_CHUNKS}==1)

class Requests:
    def __init__(self, client):
        self.client = client
        self.bearer = None
        self.user_id = None
        self.order_id = None
        self.request_id = str(uuid.uuid4())

        def next_weekday(d, weekday):
            days_ahead = weekday - d.weekday()
            if days_ahead <= 0: # Target day already happened this week
                days_ahead += 7
            return d + datetime.timedelta(days_ahead)

        tomorrow = datetime.now() + datetime.timedelta(1)
        next_monday = next_weekday(tomorrow, 0)
        self.departure_date = next_monday

    def get_name(name):
        if LOG_STATISTICS_IN_HALF_MINUTE_CHUNKS:
            now = datetime.now()
            now = datetime(now.year, now.month, now.day, now.hour, now.minute, 0 if tm.second < 30 else 30, 0)
            now_as_timestamp = int(tm.timestamp())
            return f"{name};{now_as_timestamp}"
        else:
            return name

    def home(self):
        self.client.get("/index.html", name=get_name("home"))

    def get_trip_information(self, start_at, from_station, to_station):
        head = {"Accept": "application/json", "Content-Type": "application/json"}
        body_start = {"startingPlace": from_station, "endPlace": to_station, "departureTime": start_at}

        self.client.post(url="/api/v1/travelservice/trips/left", headers=head, json=body_start, catch_response=True, name=get_name("get_trip_information"))

    def search_departure(self):
        self.get_trip_information(self.departure_date, "Shang Hai", "Su Zhou")

    def search_return(self):
        self.get_trip_information(self.departure_date, "Su Zhou", "Shang Hai")

    # def navigate_to_client_login(self):
    #     self.client.get("/client_login.html", name=get_name(sys._getframe().f_code.co_name))

    def login(self):
        # self.navigate_to_client_login()

        start_time = time.time()
        head = {"Accept": "application/json", "Content-Type": "application/json"}
        response = self.client.post(url="/api/v1/users/login", headers=head, json={"username": "fdse_microservice", "password": "111111"}, name=get_name("login"))
        response_as_json = response.json()["data"]
        if response_as_json is not None:
            token = response_as_json["token"]
            self.bearer = "Bearer " + token
            self.user_id = response_as_json["userId"]

    def book(self):
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        # self.client.get(url="/client_ticket_book.html?tripId=D1345&from=Shang%20Hai&to=Su%20Zhou&seatType=2&seat_price=50.0&date=" + self.departure_date, headers=head, name=get_name("book_ticket"))

        # get assurance types 
        self.client.get(url="/api/v1/assuranceservice/assurances/types", headers=head, name=get_name("book-get_assurance_types"))

        # get food 
        self.client.get(url="/api/v1/foodservice/foods/" + self.departure_date + "/Shang%20Hai/Su%20Zhou/D1345", headers=head, name=get_name("book-get_foods"))

        # select contact
        response_contacts = self.client.get(url="/api/v1/contactservice/contacts/account/" + self.user_id, headers=head, name=get_name("book-query_contacts"))
        response_as_json_contacts = response_contacts.json()["data"]

        if len(response_as_json_contacts) == 0:
            req_label = "set_new_contact"
            response_contacts = self.client.post(url="/api/v1/contactservice/contacts", headers=head, json={"name": self.user_id, "accountId": self.user_id, "documentType": "1", "documentNumber": self.user_id, "phoneNumber": "123456"}, name=get_name("book-set_new_contact"))

            response_as_json_contacts = response_contacts.json()["data"]
            contact_id = response_as_json_contacts["id"]
        else:
            contact_id = response_as_json_contacts[0]["id"]

        # reserve
        body_for_reservation = {"accountId": self.user_id, "contactsId": contact_id, "tripId": "D1345", "seatType": "2", "date": self.departure_date, "from": "Shang Hai", "to": "Su Zhou", "assurance": "0", "foodType": 1, "foodName": "Bone Soup", "foodPrice": 2.5, "stationName": "", "storeName": ""}
        self.client.post(url="/api/v1/preserveservice/preserve", headers=head, json=body_for_reservation, catch_response=True, name=get_name("book-preserve_ticket"))

        # Select order
        response_order_refresh = self.client.post(url="/api/v1/orderservice/order/refresh", name=get_name("book-get_order_information"), headers=head, json={"loginId": self.user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false", "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null", "boughtDateStart": "null", "boughtDateEnd": "null"})
        response_as_json = response_order_refresh.json()["data"]
        self.order_id = response_as_json[0]["id"]

        # Pay
        self.client.post(url="/api/v1/inside_pay_service/inside_payment", headers=head, json={"orderId": self.order_id, "tripId": "D1345"}, name=get_name("book-pay_order"))

    def cancel_last_order_with_no_refund(self):
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        self.client.get(url="/api/v1/cancelservice/cancel/" + self.order_id + "/" + self.user_id, headers=head, name=get_name("cancel_ticket"))

    def get_voucher(self):
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        self.client.post(url="/getVoucher", headers=head, json={"orderId": self.order_id, "type": 1}, name=get_name("get_voucher"))

    def consign_ticket(self):
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name
        self.client.get(url="/api/v1/consignservice/consigns/order/" + self.order_id, headers=head, name=get_name("consign_ticket-query"))
        self.client.put(url="/api/v1/consignservice/consigns", name=get_name("consign_ticket-create_consign"), json={"accountId": self.user_id, "handleDate": self.departure_date, "from": "Shang Hai", "to": "Su Zhou", "orderId": self.order_id, "consignee": self.order_id, "phone": "123", "weight": "1", "id": "", "isWithin": "false"}, headers=head)

    def perform_task(self, name):
        logging.debug(f"""Performing task "{name}" for user {self.request_id}...""")
        task = getattr(self, name)
        task()

# class MyHttpUser(HttpUser):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
#         self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

class UserNoLogin(HttpUser):

    @task
    def perfom_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "no login" with id {requests.request_id}...""")

        requests.perform_task("home")
        requests.perform_task("search_departure")
        requests.perform_task("search_return")


class UserBooking(HttpUser):

    @task
    def perform_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "no booking" with id {requests.request_id}...""")

        requests.perform_task("home")
        requests.perform_task("login")
        requests.perform_task("search_departure")
        requests.perform_task("book")

class UserConsignTicket(HttpUser):

    @task
    def perform_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "consign ticket" with id {requests.request_id}...""")

        requests.perform_task("home")
        requests.perform_task("login")
        requests.perform_task("search_departure")
        requests.perform_task("book")
        requests.perform_task("consign_ticket")
        

class UserCancelNoRefund(HttpUser):

    @task
    def perform_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "cancel no refund" with id {requests.request_id}...""")

        requests.perform_task("home")
        requests.perform_task("login")
        requests.perform_task("search_departure")
        requests.perform_task("book")
        requests.perform_task("cancel_last_order_with_no_refund")

class UserRefundVoucher(HttpUser):

    @task
    def perform_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "refound voucher" with id {requests.request_id}...""")

        requests.perform_task("home")
        requests.perform_task("login")
        requests.perform_task("search_departure")
        requests.perform_task("book")
        requests.perform_task("get_voucher")
