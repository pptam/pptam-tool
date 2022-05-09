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

def get_json_from_response(response):
    response_as_text = response.content.decode('UTF-8')
    response_as_json = json.loads(response_as_text)
    return response_as_json

def try_until_success(f):
    for attempt in range(100):   
        logging.debug(f"Calling function, attempt {attempt}...")
        
        try:
            result, status = f()
            if status == 1:                
                return result
            else:
                logging.debug(f"Failed, response was: {result}, trying again.")
                time.sleep(1)
        except Exception as e:
            exception_as_text = str(e)
            logging.debug(f"Failed, exception was: {exception_as_text}, trying again.")
            time.sleep(1)
        
    raise Exception("Weird... Cannot call endpoint.") 
            
def login(client):
    user_name = str(uuid.uuid4())
    password = "12345678"

    def api_call_admin_login():
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        body = {"username": "admin", "password": "222222"}
        response = client.post(url="/api/v1/users/login", headers=headers, json=body, name=get_name_suffix("admin_login"))
        response_as_json = get_json_from_response(response)
        return response_as_json, response_as_json["status"]

    response_as_json = try_until_success(api_call_admin_login)
    data = response_as_json["data"]
    token = data["token"]

    def api_call_admin_create_user():
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json", "Content-Type": "application/json"}
        body = {"documentNum": None, "documentType": 0, "email": "string", "gender": 0, "password": password, "userName": user_name}
        response = client.post(url="/api/v1/adminuserservice/users", headers=headers, json=body, name=get_name_suffix("admin_create_user"))
        return response_as_json, response_as_json["status"]
        
    response_as_json = try_until_success(api_call_admin_create_user)

    def api_call_login():
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        body = {"username": user_name, "password": password}
        response = client.post(url="/api/v1/users/login", headers=headers, json=body, name=get_name_suffix("login"))
        response_as_json = get_json_from_response(response)
        return response_as_json, response_as_json["status"]

    response_as_json = try_until_success(api_call_login)
    data = response_as_json["data"]
    user_id = data["userId"]
    token = data["token"]

    def api_call_create_contact_for_user():
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json", "Content-Type": "application/json"}
        body = {"name": user_name, "accountId": user_id, "documentType": "1", "documentNumber": "123456", "phoneNumber": "123456"}
        response = client.post(url="/api/v1/contactservice/contacts", headers=headers, json=body, name=get_name_suffix("admin_create_contact"))
        return response_as_json, response_as_json["status"]

    try_until_success(api_call_create_contact_for_user)

    return user_id, token

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

    def api_call():        
        body = {"startingPlace": from_station, "endPlace": to_station, "departureTime": departure_date}
        response = client.post(url="/api/v1/travelservice/trips/left", json=body, catch_response=True, name=get_name_suffix("get_trip_information"))
        response_as_json = get_json_from_response(response)
        return response_as_json, response_as_json["status"]

    try_until_success(api_call)

def search_departure(client):
    get_trip_information(client, "Shang Hai", "Su Zhou")

def search_return(client):
    get_trip_information(client, "Su Zhou", "Shang Hai")

def book(client, user_id):
    # we always start next Monday
    tomorrow = datetime.now() + timedelta(1)
    next_monday = next_weekday(tomorrow, 0)
    departure_date = next_monday.strftime("%Y-%m-%d")

    def api_call_insurance():
        logging.debug(f"Getting insurance types...")
        response = client.get(url="/api/v1/assuranceservice/assurances/types", name=get_name_suffix("book-get_assurance_types"))
        response_as_json = get_json_from_response(response)
        return response_as_json, response_as_json["status"]

    def api_call_food():
        logging.debug(f"Getting food types...")
        response = client.get(url="/api/v1/foodservice/foods/" + departure_date + "/Shang%20Hai/Su%20Zhou/D1345", name=get_name_suffix("book-get_foods"))
        response_as_json = get_json_from_response(response)
        return response_as_json, response_as_json["status"]

    def api_call_contacts():
        logging.debug(f"Getting contacts...")
        response = client.get(url="/api/v1/contactservice/contacts/account/" + user_id, name=get_name_suffix("book-query_contacts"))
        response_as_json = get_json_from_response(response)
        return response_as_json, response_as_json["status"]

    try_until_success(api_call_insurance)
    try_until_success(api_call_food)
    response_as_json = try_until_success(api_call_contacts)
    data = response_as_json["data"]
    contact_id = data[0]["id"] 
    
    def api_call_ticket():
        logging.debug(f"Reserving ticket...")
        body = {"accountId": user_id, "contactsId": contact_id, "tripId": "D1345", "seatType": "2", "date": departure_date, "from": "Shang Hai", "to": "Su Zhou", "assurance": "0", "foodType": 1, "foodName": "Bone Soup", "foodPrice": 2.5, "stationName": "", "storeName": ""}
        response = client.post(url="/api/v1/preserveservice/preserve", json=body, catch_response=True, name=get_name_suffix("book-preserve_ticket"))
        response_as_json = get_json_from_response(response)
        return response_as_json, response_as_json["status"]

    try_until_success(api_call_ticket)

def pay(client, user_id):
    def api_call_query():
        logging.debug(f"Getting order...")
        body = {"loginId": user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false", "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null", "boughtDateStart": "null", "boughtDateEnd": "null"}
        response = client.post(url="/api/v1/orderservice/order/refresh", json=body, name=get_name_suffix("pay-get_order_information"))
        response_as_json = get_json_from_response(response)
        return response_as_json, response_as_json["status"]

    response_as_json = try_until_success(api_call_query)
    data = response_as_json["data"]
    
    # find order that has not been paid yet
    order_id = None
    for entry in data:
        if entry["status"]==0:
            order_id = entry["id"]
            break

    if order_id == None:
        raise Exception("Weird... There is no order to pay.") 

    def api_call_pay():
        logging.debug(f"Paying order...")
        body = {"orderId": order_id, "tripId": "D1345"}
        response = client.post(url="/api/v1/inside_pay_service/inside_payment", json=body, name=get_name_suffix("book-pay_order"))
        response_as_json = get_json_from_response(response)
        return response_as_json, response_as_json["status"]

    try_until_success(api_call_pay)
        
    

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
        self.client.headers.update({"Accept": "application/json"})    

    @task
    def perfom_task(self):
        request_id = str(uuid.uuid4())
        logging.debug(f'Running user "no login" with request id {request_id}...')

        logging.debug(f'home ({request_id})...')
        home(self.client)
        logging.debug(f'search_departure ({request_id})...')
        search_departure(self.client)
        logging.debug(f'search_return ({request_id})...')
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
        request_id = str(uuid.uuid4())
        logging.debug(f'Running user "booking" with request id {request_id}...')

        logging.debug(f'home ({request_id})...')
        home(self.client)
        logging.debug(f'search_departure ({request_id})...')
        search_departure(self.client)
        logging.debug(f'search_return ({request_id})...')
        search_return(self.client)
        logging.debug(f'book ({request_id})...')
        book(self.client, self.user_id)
        logging.debug(f'pay ({request_id})...')
        pay(self.client, self.user_id)
        

# class UserConsignTicket(HttpUser):

#     def on_start(self):
#         user_id, token = login(self.client)
#         self.client.headers.update({"Authorization": f"Bearer {token}"})
#         self.client.headers.update({"Content-Type": "application/json"})   
#         self.client.headers.update({"Accept": "application/json"})   

#     @task
#     def perform_task(self):
#         requests = Requests(self.client)
#         logging.debug(f'Running user "consign ticket"')

#         requests.perform_task("home")
#         requests.perform_task("search_departure")
#         requests.perform_task("book")
#         requests.perform_task("consign_ticket")
        
# class UserCancelNoRefund(HttpUser):

#     def on_start(self):
#         user_id, token = login(self.client)
#         self.client.headers.update({"Authorization": f"Bearer {token}"})
#         self.client.headers.update({"Content-Type": "application/json"})    
#         self.client.headers.update({"Accept": "application/json"})   

#     @task
#     def perform_task(self):
#         requests = Requests(self.client)
#         logging.debug(f'Running user "cancel no refund"')

#         requests.perform_task("home")
#         requests.perform_task("search_departure")
#         requests.perform_task("book")
#         requests.perform_task("cancel_last_order_with_no_refund")

# class UserRefundVoucher(HttpUser):

#     def on_start(self):
#         user_id, token = login(self.client)
#         self.client.headers.update({"Authorization": f"Bearer {token}"})
#         self.client.headers.update({"Content-Type": "application/json"})    
#         self.client.headers.update({"Accept": "application/json"})   

#     @task
#     def perform_task(self):
#         requests = Requests(self.client)
#         logging.debug(f'Running user "voucher"')

#         requests.perform_task("home")
#         requests.perform_task("search_departure")
#         requests.perform_task("book")
#         requests.perform_task("get_voucher")

# class StagesShape(LoadTestShape):
#     """
#     A simply load test shape class that has different user and spawn_rate at
#     different stages.
#     Keyword arguments:
#         stages -- A list of dicts, each representing a stage with the following keys:
#             duration -- When this many seconds pass the test is advanced to the next stage
#             users -- Total user count
#             spawn_rate -- Number of users to start/stop per second
#             stop -- A boolean that can stop that test at a specific stage
#         stop_at_end -- Can be set to stop once all stages have run.
#     """

#     stages = [
#         {"duration": 5, "users": 10, "spawn_rate": 10},
#         {"duration": 15, "users": 50, "spawn_rate": 10},
#         {"duration": 25, "users": 100, "spawn_rate": 10}
#     ]

#     def tick(self):
#         run_time = self.get_run_time()

#         for stage in self.stages:
#             if run_time < stage["duration"]:
#                 tick_data = (stage["users"], stage["spawn_rate"])
#                 return tick_data

#         return None