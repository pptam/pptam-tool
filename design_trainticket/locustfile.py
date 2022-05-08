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
LOG_STATISTICS_IN_HALF_MINUTE_CHUNKS = (${LOG_STATISTICS_IN_HALF_MINUTE_CHUNKS}==1)

spawning_complete = False
@events.spawning_complete.add_listener
def on_spawning_complete(user_count, **kwargs):
    global spawning_complete
    spawning_complete = True

def get_data_from_response(response):
    response_as_text = response.content.decode('UTF-8')
    response_as_json = json.loads(response_as_text)
    data = response_as_json["data"]            
    return data

def login(client):
    for attempt in range(10):
        logging.debug(f"Attempt {attempt} to login...")

        try:
            headers = {"Accept": "application/json", "Content-Type": "application/json"}
            body = {"username": "fdse_microservice", "password": "111111"}
            response = client.post(url="/api/v1/users/login", headers=headers, json=body, name=get_name_suffix("login"))
            data = get_data_from_response(response)      
            user_id = data["userId"]
            token = data["token"]
            return user_id, token
        except:
            logging.debug(f"Attempt failed, retrying in 1 second...")
            time.sleep(1)

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

def get_name_suffix(name):
    global spawning_complete
    if not spawning_complete:
        name = name + "_spawning"

    if LOG_STATISTICS_IN_HALF_MINUTE_CHUNKS:
        now = datetime.now()
        now = datetime(now.year, now.month, now.day, now.hour, now.minute, 0 if now.second < 30 else 30, 0)
        now_as_timestamp = int(now.timestamp())
        return f"{name}@{now_as_timestamp}"
    else:
        return name
        
def home(client):
    client.get("/index.html", name=get_name_suffix("home"))

def get_trip_information(client, from_station, to_station):
    # we always start next Monday
    tomorrow = datetime.now() + timedelta(1)
    next_monday = next_weekday(tomorrow, 0)
    departure_date = next_monday.strftime("%Y-%m-%d")

    body_start = {"startingPlace": from_station, "endPlace": to_station, "departureTime": departure_date}
    client.post(url="/api/v1/travelservice/trips/left", json=body_start, catch_response=True, name=get_name_suffix("get_trip_information"))

def search_departure(client):
    get_trip_information(client, "Shang Hai", "Su Zhou")

def search_return(client):
    get_trip_information(client, "Su Zhou", "Shang Hai")

def book(client, user_id):
    # we always start next Monday
    tomorrow = datetime.now() + timedelta(1)
    next_monday = next_weekday(tomorrow, 0)
    departure_date = next_monday.strftime("%Y-%m-%d")

    # http://socks4.inf.unibz.it:8080/api/v1/assuranceservice/assurances/types
    response_assurances = client.get(url="/api/v1/assuranceservice/assurances/types", name=get_name_suffix("book-get_assurance_types"))
    # http://socks4.inf.unibz.it:8080/api/v1/foodservice/foods/2022-05-09/Shang%20Hai/Su%20Zhou/D1345
    response_food = client.get(url="/api/v1/foodservice/foods/" + departure_date + "/Shang%20Hai/Su%20Zhou/D1345", name=get_name_suffix("book-get_foods"))

    # http://socks4.inf.unibz.it:8080/api/v1/contactservice/contacts/account/4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f
    response_contacts = client.get(url="/api/v1/contactservice/contacts/account/" + user_id, name=get_name_suffix("book-query_contacts"))
    data = get_data_from_response(response_contacts)      
    contact_id = data[0]["id"] #4607ca48-3352-4f72-a5ee-9aa95b5f7419

    body_for_reservation = {"accountId": user_id, "contactsId": contact_id, "tripId": "D1345", "seatType": "2", "date": departure_date, "from": "Shang Hai", "to": "Su Zhou", "assurance": "0", "foodType": 1, "foodName": "Bone Soup", "foodPrice": 2.5, "stationName": "", "storeName": ""}
    response_preserve = client.post(url="/api/v1/preserveservice/preserve", json=body_for_reservation, catch_response=True, name=get_name_suffix("book-preserve_ticket"))

def pay(client, user_id):
    # http://socks4.inf.unibz.it:8080/api/v1/orderservice/order/refresh
    # {"loginId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f", "enableStateQuery": "false", "enableTravelDateQuery": "false", "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null", "boughtDateStart": "null", "boughtDateEnd": "null"}
    body_for_query = {"loginId": user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false", "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null", "boughtDateStart": "null", "boughtDateEnd": "null"}
    response_order = client.post(url="/api/v1/orderservice/order/refresh", json=body_for_query, name=get_name_suffix("pay-get_order_information"))
    data = get_data_from_response(response_order)      
    order_id = data[0]["id"]

    body_for_payment = {"orderId": order_id, "tripId": "D1345"}
    client.post(url="/api/v1/inside_pay_service/inside_payment", json=body_for_payment, name=self.get_name_suffix("book-pay_order"))


# class Requests:
#     def __init__(self, client):
#         self.client = client
#         self.request_id = str(uuid.uuid4())

#     def cancel_last_order_with_no_refund(self):
#         head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
#         self.client.get(url="/api/v1/cancelservice/cancel/" + self.order_id + "/" + self.user_id, headers=head, name=self.get_name_suffix("cancel_ticket"))

#     def get_voucher(self):
#         head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
#         self.client.post(url="/getVoucher", headers=head, json={"orderId": self.order_id, "type": 1}, name=self.get_name_suffix("get_voucher"))

#     def consign_ticket(self):
#         head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": self.bearer}
#         req_label = sys._getframe().f_code.co_name
#         self.client.get(url="/api/v1/consignservice/consigns/order/" + self.order_id, headers=head, name=self.get_name_suffix("consign_ticket-query"))
#         self.client.put(url="/api/v1/consignservice/consigns", name=self.get_name_suffix("consign_ticket-create_consign"), json={"accountId": self.user_id, "handleDate": self.departure_date, "from": "Shang Hai", "to": "Su Zhou", "orderId": self.order_id, "consignee": self.order_id, "phone": "123", "weight": "1", "id": "", "isWithin": "false"}, headers=head)



# class MyHttpUser(HttpUser):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.client.mount("https://", HTTPAdapter(pool_maxsize=50))
#         self.client.mount("http://", HTTPAdapter(pool_maxsize=50))

class UserNoLogin(HttpUser):

    def on_start(self):
        self.client.headers.update({"Content-Type": "application/json"})    

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
        self.user_id = user_id

    @task
    def perform_task(self):
        requests = Requests(self.client)
        logging.debug(f"""Running user "booking" with id {requests.request_id}...""")

        home(self.client)
        search_departure(self.client)
        search_return(self.client)
        book(self.client, self.user_id)
        

# class UserConsignTicket(HttpUser):

#     def on_start(self):
#         user_id, token = login(self.client)
#         self.client.headers.update({"Authorization": f"Bearer {token}"})
#         self.client.headers.update({"Content-Type": "application/json"})    

#     @task
#     def perform_task(self):
#         requests = Requests(self.client)
#         logging.debug(f"""Running user "consign ticket" with id {requests.request_id}...""")

#         requests.perform_task("home")
#         requests.perform_task("search_departure")
#         requests.perform_task("book")
#         requests.perform_task("consign_ticket")
        
# class UserCancelNoRefund(HttpUser):

#     def on_start(self):
#         user_id, token = login(self.client)
#         self.client.headers.update({"Authorization": f"Bearer {token}"})
#         self.client.headers.update({"Content-Type": "application/json"})    

#     @task
#     def perform_task(self):
#         requests = Requests(self.client)
#         logging.debug(f"""Running user "cancel no refund" with id {requests.request_id}...""")

#         requests.perform_task("home")
#         requests.perform_task("search_departure")
#         requests.perform_task("book")
#         requests.perform_task("cancel_last_order_with_no_refund")

# class UserRefundVoucher(HttpUser):

#     def on_start(self):
#         user_id, token = login(self.client)
#         self.client.headers.update({"Authorization": f"Bearer {token}"})
#         self.client.headers.update({"Content-Type": "application/json"})    

#     @task
#     def perform_task(self):
#         requests = Requests(self.client)
#         logging.debug(f"""Running user "refound voucher" with id {requests.request_id}...""")

#         requests.perform_task("home")
#         requests.perform_task("search_departure")
#         requests.perform_task("book")
#         requests.perform_task("get_voucher")
