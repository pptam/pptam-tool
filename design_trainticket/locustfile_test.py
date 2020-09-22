from locust import HttpUser, task, between, constant
from datetime import datetime, timedelta, date
from random import randint
import random
import json
import uuid
import numpy as np
import logging
import sys


def sequence_generator(matrix, all_functions):

    current_node = 0
    i = 0

    array = []
    array.append(all_functions[0])

    while(i < 10):
        if(1 in matrix[current_node]):
            break
        selection = random.choices(
            population=all_functions, weights=matrix[current_node])[0]
        array.append(selection)

        current_node = all_functions.index(selection)

        i += 1
    return array


class Requests():

    def home(self, _expected):
        self.client.get('/index.html')

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
                catch_response=True) as response:
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

    # user authentication

    def loginpage(self, _expected):
        self.client.get('/client_login.html')

    def admin_login(self, expected):
        if(expected):
            response1 = self.client.post(url="/api/v1/users/login",
                                         json={"username": "admin",
                                               "password": "222222"}
                                         )
        else:
            response1 = self.client.post(url="/api/v1/users/login",
                                         json={"username": "admin",
                                               "password": "WRONGPASSWORD"}
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
                                     json={"documentNum": document_num, "documentType": 0, "email": "string", "gender": 0, "password": self.user_name, "userName": self.user_name})
        response_as_json2 = json.loads(response2.content)["data"]

    def client_login(self, expected):
        if(expected):
            response = self.client.post(url="/api/v1/users/login",
                                        json={
                                            "username": self.user_name,
                                            "password": self.user_name
                                        })
        else:
            response = self.client.post(url="/api/v1/users/login",
                                        json={
                                            "username": self.user_name,
                                            # wrong password
                                            "password": "WRONGPASSWORD"
                                        })
        response_as_json = json.loads(response.content)["data"]
        token = response_as_json["token"]
        self.bearer = "Bearer " + token
        self.user_id = response_as_json["userId"]

    # purchase ticket

    def booking_page(self, _expected):
        departure_date = "2020-09-27"
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        self.client.get(
            url="/client_ticket_book.html?tripId=D1345&from=Shang%20Hai&to=Su%20Zhou&seatType=2&seat_price=50.0&date=" + departure_date,
            headers=head
        )

    def assurances(self, _expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        self.client.get(
            url="/api/v1/assuranceservice/assurances/types", headers=head)

    def foodservice(self, _expected):
        departure_date = "2020-09-27"
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        self.client.get(url="/api/v1/foodservice/foods/" +
                        departure_date + "/Shang%20Hai/Su%20Zhou/D1345", headers=head)

    def contacts(self, _expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        response_contacts = self.client.get(
            url="/api/v1/contactservice/contacts/account/" + self.user_id, headers=head)
        response_as_json_contacts = json.loads(
            response_contacts.content)["data"]

        if len(response_as_json_contacts) == 0:
            response_contacts = self.client.post(url="/api/v1/contactservice/contacts", headers=head, json={
                "name": self.user_id, "accountId": self.user_id, "documentType": "1", "documentNumber": self.user_id, "phoneNumber": "123456"})

            response_as_json_contacts = json.loads(
                response_contacts.content)["data"]
            self.contactid = response_as_json_contacts["id"]
        else:
            self.contactid = response_as_json_contacts[0]["id"]

    def reserve(self, expected):
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
                catch_response=True
        ) as response:
            if(response.status_code != 200):
                logging.debug(
                    f"Response of reserving a ticket: {response.status_code}.")

    def order_page(self, _expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        response_order_refresh = self.client.post(url="/api/v1/orderservice/order/refresh", headers=head, json={
            "loginId": self.user_id, "enableStateQuery": "false", "enableTravelDateQuery": "false", "enableBoughtDateQuery": "false", "travelDateStart": "null", "travelDateEnd": "null", "boughtDateStart": "null", "boughtDateEnd": "null"})
        response_as_json_order_id = json.loads(
            response_order_refresh.content)["data"][0]["id"]
        self.order_id = response_as_json_order_id

    def payment(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        if(expected):
            self.client.post(url="/api/v1/inside_pay_service/inside_payment",
                             headers=head, json={"orderId": self.order_id, "tripId": "D1345"})
        else:
            self.client.post(url="/api/v1/inside_pay_service/inside_payment",
                             headers=head, json={"orderId": "WRONGORDERID", "tripId": "D1345"})

    # cancelNoRefund

    def cancel_with_no_refund(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        if(expected):
            self.client.get(url="/api/v1/cancelservice/cancel/refound/" +
                            self.order_id + "/" + self.user_id, headers=head)
        else:
            self.client.get(url="/api/v1/cancelservice/cancel/refound/" +
                            self.order_id + "/" + "WRONGUSERID", headers=head)

    # user refund with voucher

    def voucher(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        if(expected):
            self.client.post(url="/getVoucher", headers=head,
                             json={"orderId": self.order_id, "type": 1})
        else:
            self.client.post(url="/getVoucher", headers=head,
                             json={"orderId": "WRONGID", "type": 1})

    # consign ticket

    def consign_page(self, _expected):
        self.client.get(
            url="/api/v1/consignservice/consigns/order/" + self.order_id)

    def confirm_consign(self, expected):
        head = {"Accept": "application/json",
                "Content-Type": "application/json", "Authorization": self.bearer}
        if(expected):
            response_as_json_consign = self.client.put(url="/api/v1/consignservice/consigns", json={"accountId": self.user_id, "handleDate": "2020-07-27", "from": "Shang Hai",
                                                                                                    "to": "Su Zhou", "orderId": self.order_id, "consignee": self.order_id, "phone": "123", "weight": "1", "id": "", "isWithin": "false"}, headers=head)
        else:
            response_as_json_consign = self.client.put(url="/api/v1/consignservice/consigns", json={"accountId": self.user_id, "handleDate": "2020-07-27", "from": "Shang Hai",
                                                                                                    "to": "Su Zhou", "orderId": self.order_id, "consignee": "WRONGORDERID", "phone": "WRONGPHONENUMBER", "weight": "1", "id": "", "isWithin": "false"}, headers=head)

    def perform_task(self, name):
        name_without_suffix = name.replace(
            "_expected", "").replace("_unexpected", "")
        task = getattr(Requests, name_without_suffix)
        task(self, name.endswith('_expected'))


class UserNoLogin(HttpUser):
    wait_time = constant(1)

    @task
    def perfom_task(self):

        matrix = np.array([[0, 0.8, 0.2, 0, 0], [0, 0, 0, 0.8, 0.2], [
                          0, 0.9, 0.1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0.9, 0.1]])
        all_functions = ["home_expected", "search_departure_expected",
                         "search_departure_unexpected", "search_return_expected", "search_return_unexpected"]
        task_sequence = sequence_generator(matrix, all_functions)
        logging.debug(
            f"Generated task sequence: {task_sequence}.")

        for task in task_sequence:
            Requests.perform_task(self, task)


class UserConsignTicket(HttpUser):
    wait_time = constant(1)

    @task
    def perform_task(self):
        matrix = np.array([[], []])
        all_functions = [
            "home_expected",
            "admin_login_expected",
            "admin_login_unexpected",
            "client_login_expected",
            "client_login_unexpected",
            "booking_page_expected",
            "search_departure_expected",
            "search_departure_unexpected",
            "booking_page_expected",
            "assurances_expected",
            "foodservice_expected",
            "contacts_expected",
            "reserve_expected",
            "reserve_unexpected",
            "order_page_expected",
            "payment_expected",
            "payment_unexpected",
            "consign_expected",
            "confirm_consign_expected",
            "confirm_consign_unexpected"
        ]
        task_sequence = sequence_generator(self, matrix, all_functions)
        logging.debug(
            f"Generated task sequence: {task_sequence}.")

        for task in task_sequence:
            perform_task(self, task)
