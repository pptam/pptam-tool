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

locust.stats.CONSOLE_STATS_INTERVAL_SEC = 30
locust.stats.CSV_STATS_FLUSH_INTERVAL_SEC = 10
locust.stats.PERCENTILES_TO_REPORT = [0.25, 0.50, 0.75, 0.80, 0.90, 0.95, 0.98, 0.99, 0.999, 0.9999, 1.0]

# Must be some days in the future.
DEP_DATE = "2022-03-11"

def random_date_generator():
    temp = randint(0, 4)
    random_y = 2000 + temp * 10 + randint(0, 9)
    random_m = randint(1, 12)
    random_d = randint(1, 28)  # to have only reasonable dates
    return str(random_y) + "-" + str(random_m) + "-" + str(random_d)


class Requests:
    def __init__(self, client):
        self.client = client
        self.bearer = None
        self.user_id = None
        self.order_id = None
        self.request_id = str(uuid.uuid4())

    def home(self):
        req_label = sys._getframe().f_code.co_name
        self.client.get("/index.html", name=req_label)

    def try_to_read_response_as_json(self, response):
        try:
            return response.json()
        except:
            try:
                return response.content.decode("utf-8")
            except:
                return response.content

    def search_ticket(self, departure_date, from_station, to_station):
        head = {"Accept": "application/json", "Content-Type": "application/json"}
        body_start = {"startingPlace": from_station, "endPlace": to_station, "departureTime": departure_date}

        req_label = sys._getframe().f_code.co_name
        self.client.post(url="/api/v1/travelservice/trips/left", headers=head, json=body_start, catch_response=True, name=req_label)

    def search_departure(self):
        self.search_ticket(date.today().strftime(random_date_generator()), "Shang Hai", "Su Zhou")

    def search_return(self):
        self.search_ticket(date.today().strftime(random_date_generator()), "Su Zhou", "Shang Hai")

    def create_user(self):
        req_label = sys._getframe().f_code.co_name
        document_num = str(uuid.uuid4())
        user_name = str(uuid.uuid4())

        response_as_json1 = None
        while response_as_json1==None or response_as_json1["status"]==0:
            time.sleep(1)
            response_as_json1 = self.client.post(url="/api/v1/users/login", json={"username": "admin", "password": "222222"}, name = req_label).json()

        token = response_as_json1["data"]["token"]
        admin_bearer = "Bearer " + token
        user_id = response_as_json1["data"]["userId"]

        self.client.post(url="/api/v1/adminuserservice/users", headers={"Authorization": admin_bearer, "Accept": "application/json", "Content-Type": "application/json"}, 
            json={"documentNum": document_num, "documentType": 0, "email": "string", "gender": 0, "password": user_name, "userName": user_name}, name=req_label)

        return user_name

    def navigate_to_client_login(self):
        req_label = sys._getframe().f_code.co_name
        self.client.get("/client_login.html", name=req_label)

    def login(self):
        user_name = self.create_user()

        self.navigate_to_client_login()
        req_label = sys._getframe().f_code.co_name
        start_time = time.time()
        head = {"Accept": "application/json", "Content-Type": "application/json"}
        response = self.client.post(url="/api/v1/users/login", headers=head, json={"username": user_name, "password": user_name}, name=req_label)
        response_as_json = response.json()["data"]
        if response_as_json is not None:
            token = response_as_json["token"]
            self.bearer = "Bearer " + token
            self.user_id = response_as_json["userId"]

    def book(self):
        departure_date = DEP_DATE
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name
        self.client.get(url="/client_ticket_book.html?tripId=D1345&from=Shang%20Hai&to=Su%20Zhou&seatType=2&seat_price=50.0&date=" + departure_date, headers=head, name=req_label)

        # get assurance types 
        self.client.get(url="/api/v1/assuranceservice/assurances/types", headers=head, name=req_label)

        # get food 
        self.client.get(url="/api/v1/foodservice/foods/" + departure_date + "/Shang%20Hai/Su%20Zhou/D1345", headers=head, name=req_label)

        # select contact
        response_contacts = self.client.get(url="/api/v1/contactservice/contacts/account/" + self.user_id, headers=head, name=req_label)
        response_as_json_contacts = response_contacts.json()["data"]

        if len(response_as_json_contacts) == 0:
            req_label = "set_new_contact"
            response_contacts = self.client.post(url="/api/v1/contactservice/contacts", headers=head, json={"name": self.user_id, "accountId": self.user_id, "documentType": "1", "documentNumber": self.user_id, "phoneNumber": "123456"}, name=req_label)

            response_as_json_contacts = response_contacts.json()["data"]
            contact_id = response_as_json_contacts["id"]
        else:
            contact_id = response_as_json_contacts[0]["id"]

        # reserve
        body_for_reservation = {"accountId": self.user_id, "contactsId": contact_id, "tripId": "D1345", "seatType": "2", "date": departure_date, "from": "Shang Hai", "to": "Su Zhou", "assurance": "0", "foodType": 1, "foodName": "Bone Soup", "foodPrice": 2.5, "stationName": "", "storeName": ""}
        self.client.post(url="/api/v1/preserveservice/preserve", headers=head, json=body_for_reservation, catch_response=True, name=req_label)

        # Select order
        response_order_refresh = self.client.post(url="/api/v1/orderservice/order/refresh", name=req_label, headers=head, json={"loginId": self.user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false", "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null", "boughtDateStart": "null", "boughtDateEnd": "null"})
        response_as_json = response_order_refresh.json()["data"]
        self.order_id = response_as_json[0]["id"]

        # Pay
        self.client.post(url="/api/v1/inside_pay_service/inside_payment", headers=head, json={"orderId": self.order_id, "tripId": "D1345"}, name=req_label)

    def cancel_last_order_with_no_refund(self):
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name
        self.client.get(url="/api/v1/cancelservice/cancel/" + self.order_id + "/" + self.user_id, headers=head, name=req_label)

    def get_voucher_of_last_order(self):
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name
        self.client.post(url="/getVoucher", headers=head, json={"orderId": self.order_id, "type": 1}, name=req_label)

    def pick_up_ticket(self):
        head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
        req_label = sys._getframe().f_code.co_name
        self.client.get(url="/api/v1/consignservice/consigns/order/" + self.order_id, headers=head, name=req_label)
        self.client.put(url="/api/v1/consignservice/consigns", name=req_label, json={"accountId": self.user_id, "handleDate": DEP_DATE, "from": "Shang Hai", "to": "Su Zhou", "orderId": self.order_id, "consignee": self.order_id, "phone": "123", "weight": "1", "id": "", "isWithin": "false"}, headers=head)

    def perform_task(self, name):
        logging.debug(f"""Performing task "{name}" for user {self.request_id}...""")
        task = getattr(self, name)
        task()


# class UserNoLogin(HttpUser):
#     weight = 1
#     wait_time = constant(1)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
#         self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

#     @task
#     def perfom_task(self):
#         requests = Requests(self.client)
#         logging.debug(f"""Running user "no login" with id {requests.request_id}...""")

#         requests.perform_task("home")
#         requests.perform_task("search_departure")
#         requests.perform_task("search_return")


class UserBooking(HttpUser):
    weight = 1
    wait_time = constant(1)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
        self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

    @task
    def perform_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "no booking" with id {requests.request_id}...""")

        requests.perform_task("home")
        requests.perform_task("login")
        requests.perform_task("search_departure")
        requests.perform_task("book")

# class UserConsignTicket(HttpUser):
#     weight = 1
#     wait_time = constant(1)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
#         self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

#     @task
#     def perform_task(self):
#         requests = Requests(self.client)
#         logging.debug(f"""Running user "consign ticket" with id {requests.request_id}...""")

#         requests.perform_task("home")
#         requests.perform_task("login")
#         requests.perform_task("search_departure")
#         requests.perform_task("book")
#         requests.perform_task("pick_up_ticket")
        

# class UserCancelNoRefund(HttpUser):
#     weight = 1
#     wait_time = constant(1)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
#         self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

#     @task
#     def perform_task(self):
#         requests = Requests(self.client)
#         logging.debug(f"""Running user "cancel no refund" with id {requests.request_id}...""")

#         requests.perform_task("home")
#         requests.perform_task("login")
#         requests.perform_task("search_departure")
#         requests.perform_task("book")
#         requests.perform_task("cancel_last_order_with_no_refund")

# class UserRefundVoucher(HttpUser):
#     weight = 1
#     wait_time = constant(1)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
#         self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

#     @task
#     def perform_task(self):
#         requests = Requests(self.client)
#         logging.debug(f"""Running user "refound voucher" with id {requests.request_id}...""")

#         requests.perform_task("home")
#         requests.perform_task("login")
#         requests.perform_task("search_departure")
#         requests.perform_task("book")
#         requests.perform_task("get_voucher_of_last_order")
