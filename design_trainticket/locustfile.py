from locust import HttpUser, task, between, constant
from datetime import datetime, timedelta, date
from random import randint
import random
import json
import uuid
import numpy as np
import logging
import sys


def matrix_checker(matrix):
    sum = np.sum(matrix, axis=1).tolist()

    return sum[1:] == sum[:-1]


def sequence_generator(matrix, all_functions):

    if(not(matrix_checker(matrix))):
        raise Exception("Matrix is not correct")

    current_node = 0
    i = 0

    array = []
    array.append(all_functions[0])

    while(i < 10):
        if(1 in matrix[current_node] and matrix[current_node].tolist().index(1) == current_node):
            break
        selection = random.choices(
            population=all_functions, weights=matrix[current_node])[0]
        array.append(selection)

        current_node = all_functions.index(selection)

        i += 1
    return array


class Requests():

    def home(self, _expected):
        self.client.get('/index.html', name=sys._getframe().f_code.co_name)

    def search_ticket(self, departure_date, from_station, to_station):
        head = {"Accept": "application/json",
                "Content-Type": "application/json"}
        body_start = {
            "startingPlace": from_station,
            "endPlace": to_station,
            "departureTime": departure_date
        }

        with self.client.post(
                url="/api/v1/travelservice/trips/left",
                headers=head,
                json=body_start,
                catch_response=True,
                name=sys._getframe().f_code.co_name) as response:
            logging.debug(
                f"Response of searching a departure ticket: {response.status_code}.")

    def search_departure(self, expected):
        if(expected):
            Requests.search_ticket(self, "2020-09-27", "Shang Hai", "Su Zhou")
        else:
            Requests.search_ticket(
                self, "2020-09-27", "DOES NOT EXIST", "Su Zhou")

    def search_return(self, expected):
        if(expected):
            Requests.search_ticket(self, "2020-09-29", "Su Zhou", "Shang Hai")
        else:
            Requests.search_ticket(
                self, "2020-09-29", "DOES NOT EXIST", "Shang Hai")

    def _create_user(self, _expected):
        response1 = self.client.post(url="/api/v1/users/login",
                                         json={"username": "admin",
                                               "password": "222222"},
                                         name="admin_login"
                                     )
        response_as_json1 = json.loads(response1.content)["data"]
        token = response_as_json1["token"]
        self.bearer = "Bearer " + token
        userrID = response_as_json1["userId"]
        document_num = str(uuid.uuid4())
        self.user_name = str(uuid.uuid4())
        response2 = self.client.post(url="/api/v1/adminuserservice/users",
                                     headers={
                                         "Authorization": self.bearer, "Accept": "application/json", "Content-Type": "application/json"},
                                     json={"documentNum": document_num, "documentType": 0, "email": "string", "gender": 0, "password": self.user_name, "userName": self.user_name},
                                     name=sys._getframe().f_code.co_name)
        response_as_json2 = json.loads(response2.content)["data"]

    def _navigate_to_client_login(self):
        self.client.get('/client_login.html', name=sys._getframe().f_code.co_name)

    def login(self, expected):
        Requests._create_user(self, expected)

        _navigate_to_client_login(self)
        if(expected):
            response = self.client.post(url="/api/v1/users/login",
                                        json={
                                            "username": self.user_name,
                                            "password": self.user_name
                                        }, name=sys._getframe().f_code.co_name)
        else:
            response = self.client.post(url="/api/v1/users/login",
                                        json={
                                            "username": self.user_name,
                                            # wrong password
                                            "password": "WRONGPASSWORD"
                                        }, name=sys._getframe().f_code.co_name)
        response_as_json = json.loads(response.content)["data"]
        token = response_as_json["token"]
        self.bearer = "Bearer " + token
        self.user_id = response_as_json["userId"]

    # purchase ticket

    def start_booking(self, _expected):
        departure_date = "2020-09-27"
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        self.client.get(
            url="/client_ticket_book.html?tripId=D1345&from=Shang%20Hai&to=Su%20Zhou&seatType=2&seat_price=50.0&date=" + departure_date,
            headers=head,
            name=sys._getframe().f_code.co_name
        )

    def get_assurance_types(self, _expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        self.client.get(
            url="/api/v1/assuranceservice/assurances/types", headers=head, name=sys._getframe().f_code.co_name)

    def get_foods(self, _expected):
        departure_date = "2020-09-27"
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        self.client.get(url="/api/v1/foodservice/foods/" +
                        departure_date + "/Shang%20Hai/Su%20Zhou/D1345", headers=head, name=sys._getframe().f_code.co_name)

    def select_contact(self, _expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        response_contacts = self.client.get(
            url="/api/v1/contactservice/contacts/account/" + self.user_id, headers=head, name=sys._getframe().f_code.co_name)
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
        departure_date = '2020-07-27'
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
                "tripId": "WRONG_TRIP_ID",
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

        with self.client.post(
                url="/api/v1/preserveservice/preserve",
                headers=head,
                json=body_for_reservation,
                catch_response=True,
                name=sys._getframe().f_code.co_name
        ) as response:
            if(response.status_code != 200):
                logging.debug(
                    f"Response of reserving a ticket: {response.status_code}.")

    def select_order(self, _expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        response_order_refresh = self.client.post(url="/api/v1/orderservice/order/refresh", name=sys._getframe().f_code.co_name, headers=head, json={
            "loginId": self.user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false", "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null", "boughtDateStart": "null", "boughtDateEnd": "null"})
        response_as_json_order_id = json.loads(
            response_order_refresh.content)["data"][0]["id"]
        self.order_id = response_as_json_order_id

    def pay(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        if(expected):
            self.client.post(url="/api/v1/inside_pay_service/inside_payment",
                             headers=head, json={"orderId": self.order_id, "tripId": "D1345"}, name=sys._getframe().f_code.co_name)
        else:
            self.client.post(url="/api/v1/inside_pay_service/inside_payment",
                             headers=head, json={"orderId": "WRONGORDERID", "tripId": "D1345"}, name=sys._getframe().f_code.co_name)

    # cancelNoRefund

    def cancel_with_no_refund(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        if(expected):
            self.client.get(url="/api/v1/cancelservice/cancel/refound/" +
                            self.order_id + "/" + self.user_id, headers=head, name=sys._getframe().f_code.co_name)
        else:
            self.client.get(url="/api/v1/cancelservice/cancel/refound/" +
                            self.order_id + "/" + "WRONGUSERID", headers=head, name=sys._getframe().f_code.co_name)

    # user refund with voucher

    def get_voucher(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        if(expected):
            self.client.post(url="/getVoucher", headers=head,
                             json={"orderId": self.order_id, "type": 1}, name=sys._getframe().f_code.co_name)
        else:
            self.client.post(url="/getVoucher", headers=head,
                             json={"orderId": "WRONGID", "type": 1}, name=sys._getframe().f_code.co_name)

    # consign ticket

    def get_consigns(self, _expected):
         self.client.get(
             url="/api/v1/consignservice/consigns/order/" + self.order_id, name=sys._getframe().f_code.co_name)

    def confirm_consign(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        if(expected):
            response_as_json_consign = self.client.put(url="/api/v1/consignservice/consigns", name=sys._getframe().f_code.co_name, json={"accountId": self.user_id, "handleDate": "2020-07-27", "from": "Shang Hai",
                                                                                                                                         "to": "Su Zhou", "orderId": self.order_id, "consignee": self.order_id, "phone": "123", "weight": "1", "id": "", "isWithin": "false"}, headers=head)
        else:
            response_as_json_consign = self.client.put(url="/api/v1/consignservice/consigns",  name=sys._getframe().f_code.co_name, json={"accountId": self.user_id, "handleDate": "2020-07-27", "from": "Shang Hai",
                                                                                                                                          "to": "Su Zhou", "orderId": self.order_id, "consignee": "WRONGORDERID", "phone": "WRONGPHONENUMBER", "weight": "1", "id": "", "isWithin": "false"}, headers=head)

    def perform_task(self, name):
        name_without_suffix = name.replace(
            "_expected", "").replace("_unexpected", "")
        task = getattr(Requests, name_without_suffix)
        task(self, name.endswith('_expected'))


class UserNoLogin(HttpUser):
    weight = 50
    wait_time = constant(1)

    @task
    def perfom_task(self):

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
        logging.debug(
            f"Generated task sequence: {task_sequence}.")
        print(task_sequence)
        for task in task_sequence:
            Requests.perform_task(self, task)


class UserBooking(HttpUser):

    weight = 50
    wait_time = constant(1)

    @task
    def perform_task(self):
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

        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_expected")] = 0.8
        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_unexpected")] = 0.2

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
        logging.debug(
            f"Generated task sequence: {task_sequence}.")
        print(task_sequence)
        for task in task_sequence:
            Requests.perform_task(self, task)


class UserConsignTicket(HttpUser):
    wait_time = constant(1)

    @task
    def perform_task(self):
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

        matrix[all_functions.index("home_expected"), all_functions.index("login_expected")] = 0.9
        matrix[all_functions.index("home_expected"), all_functions.index("login_unexpected")] = 0.1

        matrix[all_functions.index("login_unexpected"), all_functions.index("login_unexpected")] = 0.02
        matrix[all_functions.index("login_unexpected"), all_functions.index("login_expected")] = 0.98

        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_expected")] = 0.8
        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_unexpected")] = 0.2

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

        matrix[all_functions.index("pay_expected"), all_functions.index("get_consigns_expected")] = 1

        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_expected")] = 0.95

        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_unexpected")] = 0.05

        matrix[all_functions.index('get_consigns_expected'), all_functions.index('confirm_consign_expected')] = 0.9
        matrix[all_functions.index('get_consigns_expected'), all_functions.index('confirm_consign_unexpected')] = 0.1

        matrix[all_functions.index('confirm_consign_unexpected'), all_functions.index('confirm_consign_expected')] = 0.95
        matrix[all_functions.index('confirm_consign_unexpected'), all_functions.index('confirm_consign_unexpected')] = 0.05

        matrix[all_functions.index('confirm_consign_expected'), all_functions.index('confirm_consign_expected')] = 1

        
        task_sequence = sequence_generator(matrix, all_functions)
        logging.debug(
            f"Generated task sequence: {task_sequence}.")
        print(task_sequence)
        for task in task_sequence:
            Requests.perform_task(self, task)

class UserCancelNoRefund(HttpUser):
    wait_time = constant(1)

    @task
    def perform_task(self):

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

        matrix = np.zeros((len(all_functions),len(all_functions)))

        matrix[all_functions.index("home_expected"), all_functions.index("login_expected")] = 0.9
        matrix[all_functions.index("home_expected"), all_functions.index("login_unexpected")] = 0.1

        matrix[all_functions.index("login_unexpected"), all_functions.index("login_unexpected")] = 0.02
        matrix[all_functions.index("login_unexpected"), all_functions.index("login_expected")] = 0.98

        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_expected")] = 0.8
        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_unexpected")] = 0.2

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

        matrix[all_functions.index("pay_expected"), all_functions.index("cancel_with_no_refund_expected")] = 0.8
        matrix[all_functions.index("pay_expected"), all_functions.index("cancel_with_no_refund_unexpected")] = 0.2

        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_expected")] = 0.95
        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_unexpected")] = 0.05

        matrix[all_functions.index("cancel_with_no_refund_expected"), all_functions.index("cancel_with_no_refund_expected")] = 1

        matrix[all_functions.index("cancel_with_no_refund_unexpected"), all_functions.index("cancel_with_no_refund_expected")] = 0.95
        matrix[all_functions.index("cancel_with_no_refund_unexpected"), all_functions.index("cancel_with_no_refund_unexpected")] = 0.05

        
        task_sequence = sequence_generator(matrix, all_functions)
        logging.debug(
            f"Generated task sequence: {task_sequence}.")
        print(task_sequence)
        for task in task_sequence:
            Requests.perform_task(self, task)



class UserRefundVoucher(HttpUser):
    wait_time = constant(1)

    @task
    def perform_task(self):
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


        matrix = np.zeros((len(all_functions),len(all_functions)))


        matrix[all_functions.index("home_expected"), all_functions.index("login_expected")] = 0.9
        matrix[all_functions.index("home_expected"), all_functions.index("login_unexpected")] = 0.1

        matrix[all_functions.index("login_unexpected"), all_functions.index("login_unexpected")] = 0.02
        matrix[all_functions.index("login_unexpected"), all_functions.index("login_expected")] = 0.98

        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_expected")] = 0.8
        matrix[all_functions.index("login_expected"), all_functions.index("search_departure_unexpected")] = 0.2

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

        matrix[all_functions.index("pay_expected"), all_functions.index("get_voucher_expected")] = 0.8
        matrix[all_functions.index("pay_expected"), all_functions.index("get_voucher_unexpected")] = 0.2

        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_expected")] = 0.95
        matrix[all_functions.index("pay_unexpected"), all_functions.index("pay_unexpected")] = 0.05

        matrix[all_functions.index("get_voucher_expected"), all_functions.index("get_voucher_expected")] = 1

        matrix[all_functions.index("get_voucher_unexpected"), all_functions.index("get_voucher_expected")] = 0.95
        matrix[all_functions.index("get_voucher_unexpected"), all_functions.index("get_voucher_unexpected")] = 0.05

        
        task_sequence = sequence_generator(matrix, all_functions)
        logging.debug(
            f"Generated task sequence: {task_sequence}.")
        print(task_sequence)
        for task in task_sequence:
            Requests.perform_task(self, task)


