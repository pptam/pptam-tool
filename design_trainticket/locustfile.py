from locust import HttpUser, task, between, constant
from datetime import datetime, timedelta, date
from random import randint
import random
import json
import uuid
import numpy as np
import logging
import sys
import time
import os
import string
import logging

DEP_DATE = "2020-11-27"

def matrix_checker(matrix):
    sum = np.sum(matrix, axis=1).tolist()

    return sum[1:] == sum[:-1]


def sequence_generator(matrix, all_functions):

    if(not(matrix_checker(matrix))):
        raise Exception("Matrix is not correct")

    max_sequence_len = 20
    current_node = 0
    i = 0

    array = []
    array.append(all_functions[0])

    while(i < max_sequence_len):
        if(1 in matrix[current_node] and matrix[current_node].tolist().index(1) == current_node):
            break
        selection = random.choices(
            population=all_functions, weights=matrix[current_node])[0]
        array.append(selection)

        current_node = all_functions.index(selection)

        i += 1
    return array


def do_log(logDict: dict):
    logging.debug(json.dumps(logDict))


def random_string_generator():
    len = randint(8, 16)
    prob = randint(0, 100)
    if(prob < 25):
        random_string = ''.join([random.choice(string.ascii_letters) for n in range(len)])
    elif(prob < 50):
        random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(len)])
    elif(prob < 75):
        random_string = ''.join([random.choice(string.ascii_letters + string.digits + string.punctuation) for n in range(len)])
    else:
        random_string = ''
    return random_string


def random_date_generator():
    temp = randint(0, 4)
    random_y = 2000 + temp*10 + randint(0, 9)
    random_m = randint(1, 12)
    random_d = randint(1, 31)  # assumendo che la data possa essere non sensata (e.g. 30 Febbraio)
    return str(random_y)+'-'+str(random_m)+'-'+str(random_d)

def postfix(expected = True):
    if expected:
        return '_expected'
    return '_unexpected'


class Requests():

    def home(self, expected):

        start_time = time.time()
        with self.client.get('/index.html', name=sys._getframe().f_code.co_name) as response:
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected,  'status_code': response.status_code, 'response_time': time.time() - start_time, })

    def search_ticket(self, departure_date, from_station, to_station, expected = True):
        head = {"Accept": "application/json",
                "Content-Type": "application/json"}
        body_start = {
            "startingPlace": from_station,
            "endPlace": to_station,
            "departureTime": departure_date
        }

        start_time = time.time()

        with self.client.post(
                url="/api/v1/travelservice/trips/left",
                headers=head,
                json=body_start,
                catch_response=True,
                name=sys._getframe().f_code.co_name) as response:
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                    'response_time': time.time() - start_time,  'response': json.loads((response.content).decode('utf-8'))})

    def search_departure(self, expected):
        if(expected):
            Requests.search_ticket(self, date.today().strftime(random_date_generator()), "Shang Hai", "Su Zhou", expected)
        else:
            Requests.search_ticket(
                self, date.today().strftime(random_date_generator()), random_string_generator(), "Su Zhou", expected)

    def search_return(self, expected):
        if(expected):
            Requests.search_ticket(self, date.today().strftime(random_date_generator()), "Su Zhou", "Shang Hai", expected)
        else:
            Requests.search_ticket(
                self, date.today().strftime(random_date_generator()), random_string_generator(), "Shang Hai", expected)

    def _create_user(self, expected):
        start_time = time.time()
        with self.client.post(url="/api/v1/users/login",
                              json={"username": "admin",
                                    "password": "222222"},
                              name="admin_login"
                              ) as response1:
            do_log({'name': '_admin_login' + postfix(expected), 'expected': expected, 'status_code': response1.status_code,
                    'response_time': time.time() - start_time, 'response': json.loads((response1.content).decode('utf-8'))})

            response_as_json1 = json.loads(response1.content)["data"]
            token = response_as_json1["token"]
            self.bearer = "Bearer " + token
            userrID = response_as_json1["userId"]
            document_num = str(uuid.uuid4())
            self.user_name = str(uuid.uuid4())
        start_time = time.time()
        with self.client.post(url="/api/v1/adminuserservice/users",
                              headers={
                                  "Authorization": self.bearer, "Accept": "application/json", "Content-Type": "application/json"},
                              json={"documentNum": document_num, "documentType": 0, "email": "string", "gender": 0, "password": self.user_name, "userName": self.user_name},
                              name=sys._getframe().f_code.co_name) as response2:
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response2.status_code,
                    'response_time': time.time() - start_time, 'response': json.loads((response2.content).decode('utf-8'))})
            response_as_json2 = json.loads(response2.content)["data"]

    def _navigate_to_client_login(self, expected = True):
        start_time = time.time()
        with self.client.get('/client_login.html', name=sys._getframe().f_code.co_name) as response:
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': True,  'status_code': response.status_code, 'response_time': time.time() - start_time, })

    def login(self, expected):
        Requests._create_user(self, expected)

        Requests._navigate_to_client_login(self)
        start_time = time.time()
        if(expected):
            response = self.client.post(url="/api/v1/users/login",
                                        json={
                                            "username": self.user_name,
                                            "password": self.user_name
                                        }, name=sys._getframe().f_code.co_name)
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                    'response_time': time.time() - start_time, 'response': json.loads((response.content).decode('utf-8'))})
        else:
            response = self.client.post(url="/api/v1/users/login",
                                        json={
                                            "username": self.user_name,
                                            # wrong password
                                            "password": random_string_generator()
                                        }, name=sys._getframe().f_code.co_name)
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                    'response_time': time.time() - start_time, 'response': json.loads((response.content).decode('utf-8'))})

        response_as_json = json.loads(response.content)["data"]
        if response_as_json is not None:
            token = response_as_json["token"]
            self.bearer = "Bearer " + token
            self.user_id = response_as_json["userId"]

    # purchase ticket

    def start_booking(self, expected):
        departure_date = DEP_DATE
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        with self.client.get(
            url="/client_ticket_book.html?tripId=D1345&from=Shang%20Hai&to=Su%20Zhou&seatType=2&seat_price=50.0&date=" + departure_date,
            headers=head,
            name=sys._getframe().f_code.co_name
        ) as response:
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code, 'response_time': time.time() - start_time, })

    def get_assurance_types(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        with self.client.get(
                url="/api/v1/assuranceservice/assurances/types", headers=head, name=sys._getframe().f_code.co_name) as response:
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                    'response_time': time.time() - start_time, 'response': json.loads((response.content).decode('utf-8'))})

    def get_foods(self, expected):
        departure_date = DEP_DATE
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        with self.client.get(url="/api/v1/foodservice/foods/" +
                             departure_date + "/Shang%20Hai/Su%20Zhou/D1345", headers=head, name=sys._getframe().f_code.co_name) as response:
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                    'response_time': time.time() - start_time, 'response': json.loads((response.content).decode('utf-8'))})

    def select_contact(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response_contacts = self.client.get(
            url="/api/v1/contactservice/contacts/account/" + self.user_id, headers=head, name=sys._getframe().f_code.co_name)
        do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response_contacts.status_code,
                'response_time': time.time() - start_time,  'response': json.loads((response_contacts.content).decode('utf-8'))})

        response_as_json_contacts = json.loads(
            response_contacts.content)["data"]

        if len(response_as_json_contacts) == 0:
            response_contacts = self.client.post(url="/api/v1/contactservice/contacts", headers=head, json={
                "name": self.user_id, "accountId": self.user_id, "documentType": "1", "documentNumber": self.user_id, "phoneNumber": "123456"}, name="set_new_contact")

            response_as_json_contacts = json.loads(
                response_contacts.content)["data"]
            self.contactid = response_as_json_contacts["id"]
        else:
            self.contactid = response_as_json_contacts[0]["id"]

    def finish_booking(self, expected):
        departure_date = DEP_DATE
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        if(expected):
            body_for_reservation = {
                "accountId": self.user_id,
                "contactsId": self.contactid,
                "tripId": "D1345",
                "seatType": "2",
                "date": departure_date,
                "from": "Shang Hai",
                "to": "Su Zhou",
                "assurance": "0",
                "foodType": 1,
                "foodName": "Bone Soup",
                "foodPrice": 2.5,
                "stationName": "",
                "storeName": ""
            }
        else:
            body_for_reservation = {
                "accountId": self.user_id,
                "contactsId": self.contactid,
                "tripId": random_string_generator(),
                "seatType": "2",
                "date": departure_date,
                "from": "Shang Hai",
                "to": "Su Zhou",
                "assurance": "0",
                "foodType": 1,
                "foodName": "Bone Soup",
                "foodPrice": 2.5,
                "stationName": "",
                "storeName": ""
            }
        start_time = time.time()
        with self.client.post(
                url="/api/v1/preserveservice/preserve",
                headers=head,
                json=body_for_reservation,
                catch_response=True,
                name=sys._getframe().f_code.co_name
        ) as response:
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                    'response_time': time.time() - start_time, 'response': json.loads((response.content).decode('utf-8'))})

    def select_order(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        response_order_refresh = self.client.post(url="/api/v1/orderservice/order/refresh", name=sys._getframe().f_code.co_name, headers=head, json={
            "loginId": self.user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false", "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null", "boughtDateStart": "null", "boughtDateEnd": "null"})

        do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response_order_refresh.status_code,
                'response_time': time.time() - start_time,  'response': json.loads((response_order_refresh.content).decode('utf-8'))})

        response_order_refresh_content = json.loads(response_order_refresh.content)
        print(json.dumps(response_order_refresh_content))
        response_as_json_order_id = response_order_refresh_content["data"][0]["id"]
        self.order_id = response_as_json_order_id

    def pay(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        if(expected):
            with self.client.post(url="/api/v1/inside_pay_service/inside_payment",
                                  headers=head, json={"orderId": self.order_id, "tripId": "D1345"}, name=sys._getframe().f_code.co_name) as response:
                do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                        'response_time': time.time() - start_time, 'response': json.loads((response.content).decode('utf-8'))})

        else:
            with self.client.post(url="/api/v1/inside_pay_service/inside_payment",
                                  headers=head, json={"orderId": random_string_generator(), "tripId": "D1345"}, name=sys._getframe().f_code.co_name) as response:
                do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                        'response_time': time.time() - start_time,  'response': json.loads((response.content).decode('utf-8'))})

    # cancelNoRefund

    def cancel_with_no_refund(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        if(expected):
            with self.client.get(url="/api/v1/cancelservice/cancel/refound/" +
                                 self.order_id + "/" + self.user_id, headers=head, name=sys._getframe().f_code.co_name) as response:
                do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                        'response_time': time.time() - start_time, 'response': json.loads((response.content).decode('utf-8'))})

        else:
            with self.client.get(url="/api/v1/cancelservice/cancel/refound/" +
                                 self.order_id + "/" + random_string_generator(), headers=head, name=sys._getframe().f_code.co_name) as response:
                do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                        'response_time': time.time() - start_time, 'response': json.loads((response.content).decode('utf-8'))})

    # user refund with voucher

    def get_voucher(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        if(expected):
            with self.client.post(url="/getVoucher", headers=head,
                                  json={"orderId": self.order_id, "type": 1}, name=sys._getframe().f_code.co_name) as response:
                do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                        'response_time': time.time() - start_time, 'response': json.loads((response.content).decode('utf-8'))})

        else:
            with self.client.post(url="/getVoucher", headers=head,
                                  json={"orderId": random_string_generator(), "type": 1}, name=sys._getframe().f_code.co_name) as response:
                do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                        'response_time': time.time() - start_time, 'response': None})

    # consign ticket

    def get_consigns(self, expected):
        start_time = time.time()
        with self.client.get(
                url="/api/v1/consignservice/consigns/order/" + self.order_id, name=sys._getframe().f_code.co_name) as response:
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response.status_code,
                    'response_time': time.time() - start_time, 'response': json.loads((response.content).decode('utf-8'))})

    def confirm_consign(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        start_time = time.time()
        if(expected):
            response_as_json_consign = self.client.put(url="/api/v1/consignservice/consigns", name=sys._getframe().f_code.co_name, json={"accountId": self.user_id, "handleDate": DEP_DATE, "from": "Shang Hai",
                                                                                                                                         "to": "Su Zhou", "orderId": self.order_id, "consignee": self.order_id, "phone": "123", "weight": "1", "id": "", "isWithin": "false"}, headers=head)
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response_as_json_consign.status_code,
                    'response_time': time.time() - start_time, 'response': json.loads((response_as_json_consign.content).decode('utf-8'))})

        else:
            response_as_json_consign = self.client.put(url="/api/v1/consignservice/consigns",  name=sys._getframe().f_code.co_name, json={"accountId": self.user_id, "handleDate": DEP_DATE, "from": "Shang Hai",
                                                                                                                                          "to": "Su Zhou", "orderId": self.order_id, "consignee": random_string_generator(), "phone": random_string_generator(), "weight": "1", "id": "", "isWithin": "false"}, headers=head)
            do_log({'name': sys._getframe().f_code.co_name + postfix(expected), 'expected': expected, 'status_code': response_as_json_consign.status_code,
                    'response_time': time.time() - start_time, 'response': json.loads((response_as_json_consign.content).decode('utf-8'))})

    def perform_task(self, name):
        name_without_suffix = name.replace(
            "_expected", "").replace("_unexpected", "")
        task = getattr(Requests, name_without_suffix)
        task(self, name.endswith('_expected'))


class UserNoLogin(HttpUser):
    wait_time = constant(1)

    @task
    def perfom_task(self):
        logging.debug("Running user 'no login'...")

        all_functions = ["home_expected", "search_departure_expected",
                         "search_departure_unexpected", "search_return_expected", "search_return_unexpected"]

        matrix = np.zeros((len(all_functions), len(all_functions)))

        matrix[all_functions.index("home_expected"), all_functions.index("search_departure_expected")] = 0.8
        matrix[all_functions.index("home_expected"), all_functions.index("search_departure_unexpected")] = 0.2

        matrix[all_functions.index("search_departure_expected"), all_functions.index("search_return_expected")] = 0.8
        matrix[all_functions.index("search_departure_expected"), all_functions.index("search_return_unexpected")] = 0.2

        matrix[all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_expected")] = 0.9
        matrix[all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_unexpected")] = 0.1

        matrix[all_functions.index("search_return_expected"), all_functions.index("search_return_expected")] = 1
        matrix[all_functions.index("search_return_unexpected"), all_functions.index("search_return_expected")] = 0.9
        matrix[all_functions.index("search_return_unexpected"), all_functions.index("search_return_unexpected")] = 0.1

        task_sequence = sequence_generator(matrix, all_functions)

        for task in task_sequence:
            Requests.perform_task(self, task)


class UserBooking(HttpUser):
    wait_time = constant(1)

    @task
    def perform_task(self):
        logging.debug("Running user 'booking'...")

        all_functions = [
            "home_expected",
            "login_expected",
            "login_unexpected",
            "search_departure_expected",
            "search_departure_unexpected",
            "start_booking_expected",
            "get_assurance_types_expected",
            "get_foods_expected",
            "select_contact_expected",
            "finish_booking_expected",
            "finish_booking_unexpected",
            "select_order_expected",
            "pay_expected",
            "pay_unexpected",
        ]
        matrix = np.zeros((len(all_functions), len(all_functions)))

        matrix[all_functions.index("home_expected"), all_functions.index("login_expected")] = 0.9
        matrix[all_functions.index("home_expected"), all_functions.index("login_unexpected")] = 0.1

        matrix[all_functions.index("login_unexpected"), all_functions.index("login_unexpected")] = 0.02
        matrix[all_functions.index("login_unexpected"), all_functions.index("login_expected")] = 0.98

        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_expected")] = 0.9  # 0.8
        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_unexpected")] = 0.1  # 0.2

        matrix[all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_expected")] = 0.95
        matrix[all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_unexpected")] = 0.05

        matrix[all_functions.index("search_departure_expected"), all_functions.index("start_booking_expected")] = 1

        matrix[all_functions.index("start_booking_expected"), all_functions.index("get_assurance_types_expected")] = 1

        matrix[all_functions.index("get_assurance_types_expected"), all_functions.index("get_foods_expected")] = 1

        matrix[all_functions.index("get_foods_expected"), all_functions.index("select_contact_expected")] = 1

        matrix[all_functions.index("select_contact_expected"), all_functions.index("finish_booking_expected")] = 0.8

        matrix[all_functions.index("select_contact_expected"), all_functions.index("finish_booking_unexpected")] = 0.2

        matrix[all_functions.index("finish_booking_unexpected"), all_functions.index("finish_booking_expected")] = 0.95
        matrix[all_functions.index("finish_booking_unexpected"), all_functions.index("finish_booking_unexpected")] = 0.05

        matrix[all_functions.index("finish_booking_expected"), all_functions.index("select_order_expected")] = 1

        matrix[all_functions.index("select_order_expected"), all_functions.index("pay_expected")] = 0.8
        matrix[all_functions.index("select_order_expected"), all_functions.index("pay_unexpected")] = 0.2

        matrix[all_functions.index("pay_expected"), all_functions.index("pay_expected")] = 1

        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_expected")] = 0.95

        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_unexpected")] = 0.05

        task_sequence = sequence_generator(matrix, all_functions)

        for task in task_sequence:
            Requests.perform_task(self, task)


class UserConsignTicket(HttpUser):
    wait_time = constant(1)

    @task
    def perform_task(self):
        logging.debug("Running user 'consign ticket'...")
        all_functions = [
            "home_expected",
            "login_expected",
            "login_unexpected",
            "search_departure_expected",
            "search_departure_unexpected",
            "start_booking_expected",
            "get_assurance_types_expected",
            "get_foods_expected",
            "select_contact_expected",
            "finish_booking_expected",
            "finish_booking_unexpected",
            "select_order_expected",
            "pay_expected",
            "pay_unexpected",
            "get_consigns_expected",
            "confirm_consign_expected",
            "confirm_consign_unexpected"
        ]
        matrix = np.zeros((len(all_functions), len(all_functions)))

        matrix[all_functions.index("home_expected"), all_functions.index("login_expected")] = 0.8  # 0.9
        matrix[all_functions.index("home_expected"), all_functions.index("login_unexpected")] = 0.2  # 0.1

        matrix[all_functions.index("login_unexpected"), all_functions.index("login_unexpected")] = 0.15  # 0.02
        matrix[all_functions.index("login_unexpected"), all_functions.index("login_expected")] = 0.85  # 0.98

        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_expected")] = 0.7  # 0.8
        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_unexpected")] = 0.3  # 0.2

        matrix[all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_expected")] = 0.85  # 0.95
        matrix[all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_unexpected")] = 0.15  # 0.05

        matrix[all_functions.index("search_departure_expected"), all_functions.index("start_booking_expected")] = 1

        matrix[all_functions.index("start_booking_expected"), all_functions.index("get_assurance_types_expected")] = 1

        matrix[all_functions.index("get_assurance_types_expected"), all_functions.index("get_foods_expected")] = 1

        matrix[all_functions.index("get_foods_expected"), all_functions.index("select_contact_expected")] = 1

        matrix[all_functions.index("select_contact_expected"), all_functions.index("finish_booking_expected")] = 0.75  # 0.8

        matrix[all_functions.index("select_contact_expected"), all_functions.index("finish_booking_unexpected")] = 0.25  # 0.2

        matrix[all_functions.index("finish_booking_unexpected"), all_functions.index("finish_booking_expected")] = 0.9  # 0.95
        matrix[all_functions.index("finish_booking_unexpected"), all_functions.index("finish_booking_unexpected")] = 0.1  # 0.05

        matrix[all_functions.index("finish_booking_expected"), all_functions.index("select_order_expected")] = 1

        matrix[all_functions.index("select_order_expected"), all_functions.index("pay_expected")] = 0.7  # 0.8
        matrix[all_functions.index("select_order_expected"), all_functions.index("pay_unexpected")] = 0.3  # 0.2

        matrix[all_functions.index("pay_expected"), all_functions.index("get_consigns_expected")] = 1

        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_expected")] = 0.85  # 0.95
        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_unexpected")] = 0.15  # 0.05

        matrix[all_functions.index('get_consigns_expected'), all_functions.index('confirm_consign_expected')] = 0.8  # 0.9
        matrix[all_functions.index('get_consigns_expected'), all_functions.index('confirm_consign_unexpected')] = 0.2  # 0.1

        matrix[all_functions.index('confirm_consign_unexpected'), all_functions.index('confirm_consign_expected')] = 0.9  # 0.95
        matrix[all_functions.index('confirm_consign_unexpected'), all_functions.index('confirm_consign_unexpected')] = 0.1  # 0.05

        matrix[all_functions.index('confirm_consign_expected'), all_functions.index('confirm_consign_expected')] = 1

        task_sequence = sequence_generator(matrix, all_functions)

        for task in task_sequence:
            Requests.perform_task(self, task)


class UserCancelNoRefund(HttpUser):
    wait_time = constant(1)

    @task
    def perform_task(self):
        logging.debug("Running user 'cancel no refund'...")

        all_functions = [
            "home_expected",
            "login_expected",
            "login_unexpected",
            "search_departure_expected",
            "search_departure_unexpected",
            "start_booking_expected",
            "get_assurance_types_expected",
            "get_foods_expected",
            "select_contact_expected",
            "finish_booking_expected",
            "finish_booking_unexpected",
            "select_order_expected",
            "pay_expected",
            "pay_unexpected",
            "cancel_with_no_refund_expected",
            "cancel_with_no_refund_unexpected"
        ]

        matrix = np.zeros((len(all_functions), len(all_functions)))

        matrix[all_functions.index("home_expected"), all_functions.index("login_expected")] = 0.99  # 0.9
        matrix[all_functions.index("home_expected"), all_functions.index("login_unexpected")] = 0.01  # 0.1

        matrix[all_functions.index("login_unexpected"), all_functions.index("login_unexpected")] = 0.001  # 0.02
        matrix[all_functions.index("login_unexpected"), all_functions.index("login_expected")] = 0.999  # 0.98

        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_expected")] = 0.9  # 0.8
        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_unexpected")] = 0.1  # 0.2

        matrix[all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_expected")] = 0.99  # 0.95
        matrix[all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_unexpected")] = 0.01  # 0.05

        matrix[all_functions.index("search_departure_expected"), all_functions.index("start_booking_expected")] = 1

        matrix[all_functions.index("start_booking_expected"), all_functions.index("get_assurance_types_expected")] = 1

        matrix[all_functions.index("get_assurance_types_expected"), all_functions.index("get_foods_expected")] = 1

        matrix[all_functions.index("get_foods_expected"), all_functions.index("select_contact_expected")] = 1

        matrix[all_functions.index("select_contact_expected"), all_functions.index("finish_booking_expected")] = 0.99  # 0.8
        matrix[all_functions.index("select_contact_expected"), all_functions.index("finish_booking_unexpected")] = 0.01  # 0.2

        matrix[all_functions.index("finish_booking_unexpected"), all_functions.index("finish_booking_expected")] = 0.99  # 0.95
        matrix[all_functions.index("finish_booking_unexpected"), all_functions.index("finish_booking_unexpected")] = 0.01  # 0.05

        matrix[all_functions.index("finish_booking_expected"), all_functions.index("select_order_expected")] = 1

        matrix[all_functions.index("select_order_expected"), all_functions.index("pay_expected")] = 0.99  # 0.8
        matrix[all_functions.index("select_order_expected"), all_functions.index("pay_unexpected")] = 0.01  # 0.2

        matrix[all_functions.index("pay_expected"), all_functions.index("cancel_with_no_refund_expected")] = 0.99  # 0.8
        matrix[all_functions.index("pay_expected"), all_functions.index("cancel_with_no_refund_unexpected")] = 0.01  # 0.2

        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_expected")] = 0.99  # 0.95
        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_unexpected")] = 0.01  # 0.05

        matrix[all_functions.index("cancel_with_no_refund_expected"), all_functions.index("cancel_with_no_refund_expected")] = 1

        matrix[all_functions.index("cancel_with_no_refund_unexpected"), all_functions.index("cancel_with_no_refund_expected")] = 0.99  # 0.95
        matrix[all_functions.index("cancel_with_no_refund_unexpected"), all_functions.index("cancel_with_no_refund_unexpected")] = 0.01  # 0.05

        task_sequence = sequence_generator(matrix, all_functions)

        for task in task_sequence:
            Requests.perform_task(self, task)


class UserRefundVoucher(HttpUser):
    wait_time = constant(1)

    @task
    def perform_task(self):
        logging.debug("Running user 'refound voucher'...")

        all_functions = [
            "home_expected",
            "login_expected",
            "login_unexpected",
            "search_departure_expected",
            "search_departure_unexpected",
            "start_booking_expected",
            "get_assurance_types_expected",
            "get_foods_expected",
            "select_contact_expected",
            "finish_booking_expected",
            "finish_booking_unexpected",
            "select_order_expected",
            "pay_expected",
            "pay_unexpected",
            "get_voucher_expected",
            "get_voucher_unexpected"
        ]

        matrix = np.zeros((len(all_functions), len(all_functions)))

        matrix[all_functions.index("home_expected"), all_functions.index("login_expected")] = 0.85  # 0.9
        matrix[all_functions.index("home_expected"), all_functions.index("login_unexpected")] = 0.15  # 0.1

        matrix[all_functions.index("login_unexpected"), all_functions.index("login_unexpected")] = 0.1  # 0.02
        matrix[all_functions.index("login_unexpected"), all_functions.index("login_expected")] = 0.9  # 0.98

        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_expected")] = 0.85  # 0.8
        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_unexpected")] = 0.15  # 0.2

        matrix[all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_expected")] = 0.9  # 0.95
        matrix[all_functions.index("search_departure_unexpected"), all_functions.index("search_departure_unexpected")] = 0.1  # 0.05

        matrix[all_functions.index("search_departure_expected"), all_functions.index("start_booking_expected")] = 1

        matrix[all_functions.index("start_booking_expected"), all_functions.index("get_assurance_types_expected")] = 1

        matrix[all_functions.index("get_assurance_types_expected"), all_functions.index("get_foods_expected")] = 1

        matrix[all_functions.index("get_foods_expected"), all_functions.index("select_contact_expected")] = 1

        matrix[all_functions.index("select_contact_expected"), all_functions.index("finish_booking_expected")] = 0.8

        matrix[all_functions.index("select_contact_expected"), all_functions.index("finish_booking_unexpected")] = 0.2

        matrix[all_functions.index("finish_booking_unexpected"), all_functions.index("finish_booking_expected")] = 0.95
        matrix[all_functions.index("finish_booking_unexpected"), all_functions.index("finish_booking_unexpected")] = 0.05

        matrix[all_functions.index("finish_booking_expected"), all_functions.index("select_order_expected")] = 1

        matrix[all_functions.index("select_order_expected"), all_functions.index("pay_expected")] = 0.8
        matrix[all_functions.index("select_order_expected"), all_functions.index("pay_unexpected")] = 0.2

        matrix[all_functions.index("pay_expected"), all_functions.index("get_voucher_expected")] = 0.8
        matrix[all_functions.index("pay_expected"), all_functions.index("get_voucher_unexpected")] = 0.2

        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_expected")] = 0.9  # 0.95
        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_unexpected")] = 0.1  # 0.05

        matrix[all_functions.index("get_voucher_expected"), all_functions.index("get_voucher_expected")] = 1

        matrix[all_functions.index("get_voucher_unexpected"), all_functions.index("get_voucher_expected")] = 0.85  # 0.95
        matrix[all_functions.index("get_voucher_unexpected"), all_functions.index("get_voucher_unexpected")] = 0.15  # 0.05

        task_sequence = sequence_generator(matrix, all_functions)

        for task in task_sequence:
            Requests.perform_task(self, task)
