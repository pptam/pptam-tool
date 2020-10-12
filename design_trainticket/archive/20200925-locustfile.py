from locust import HttpUser, task, between
from datetime import datetime, timedelta, date
from random import randint
import random
import json
import uuid
import numpy as np
import random


def authentication(self):

        matrix = np.array([[0.2,0.8], [0.05,0.95]])

        response1 = self.client.post(url="/api/v1/users/login", json={"username": "admin", "password": "222222"})
        response_as_json1 = json.loads(response1.content)["data"]
        token = response_as_json1["token"]
        self.bearer = "Bearer " + token
        userrID = response_as_json1["userId"]

        document_num = str(uuid.uuid4())
        user_name = str(uuid.uuid4())

        response2 = self.client.post(url="/api/v1/adminuserservice/users", headers={"Authorization": self.bearer, "Accept": "application/json", "Content-Type": "application/json"}, json={"documentNum": document_num, "documentType": 0, "email": "string", "gender": 0, "password": user_name, "userName": user_name})
        response_as_json2 = json.loads(response2.content)["data"]

        # Removes trailing / from the host name to avoid exceptions in the tests
        self.host = self.host.rstrip("/")

        self.client.get('/client_login.html')

        
        if(random.random() > matrix[0,0]):
           response = self.client.post(url="/api/v1/users/login",
                                    json={
                                        "username": user_name,
                                        "password": user_name
                                    })
        else:
            response = self.client.post(url="/api/v1/users/login",
                                    json={
                                        "username": user_name,
                                        "password": "test"
                                    })
            if(random.random() > matrix[1,0]):
               response = self.client.post(url="/api/v1/users/login",
                                    json={
                                        "username": user_name,
                                        "password": user_name
                                    })

            else:
               response = self.client.post(url="/api/v1/users/login",
                                    json={
                                        "username": user_name,
                                        "password": "test"
                                    })


        response_as_json = json.loads(response.content)["data"]
        token = response_as_json["token"]
        self.bearer = "Bearer " + token
        self.user_id = response_as_json["userId"]


def purchaseTicket(self):


        self.client.get('/index.html')
        
        departure_date = '2020-09-18'

        head = {"Accept": "application/json", "Content-Type":"application/json","Authorization": self.bearer}
        body_start = {
            "startingPlace": "Shang Hai", 
            "endPlace": "Su Zhou",
            "departureTime": departure_date
            }
        

        with self.client.post(
            url="/api/v1/travelservice/trips/left", 
            headers=head, 
            json=body_start, 
            catch_response=True) as response:
            if response.status_code != 200:
                print(response.status_code)

        self.client.get(
            url="/client_ticket_book.html?tripId=D1345&from=Shang%20Hai&to=Su%20Zhou&seatType=2&seat_price=50.0&date="+ departure_date,
            headers=head
            )

        self.client.get(url="/api/v1/assuranceservice/assurances/types",headers=head)
        self.client.get(url="/api/v1/foodservice/foods/"+ departure_date  + "/Shang%20Hai/Su%20Zhou/D1345", headers=head)
        


        response_contacts = self.client.get(url="/api/v1/contactservice/contacts/account/" + self.user_id, headers=head)


        
        response_as_json_contacts = json.loads(response_contacts.content)["data"]


        if len(response_as_json_contacts) == 0:
            response_contacts = self.client.post(url="/api/v1/contactservice/contacts", headers=head, json={"name":self.user_id,"accountId": self.user_id,"documentType":"1","documentNumber":self.user_id,"phoneNumber":"123456"})


            response_as_json_contacts = json.loads(response_contacts.content)["data"]
            self.contactid = response_as_json_contacts["id"]
            print('test')
            print(self.contactid)
        else:
            self.contactid = response_as_json_contacts[0]["id"]
            print(self.contactid)
        

        
        
        body_for_reservation = {
        "accountId": self.user_id,
        "contactsId": self.contactid,
        "tripId":"D1345",
        "seatType":"2",
        "date":departure_date,
        "from":"Shang Hai",
        "to":"Su Zhou",
        "assurance":"0",
        "foodType":1,
        "foodName":"Bone Soup",
        "foodPrice":2.5,
        "stationName":"",
        "storeName":""
        }

        with self.client.post(
            url="/api/v1/preserveservice/preserve",
            headers=head,
            json=body_for_reservation,
            catch_response=True
            ) as response:
            if(response.status_code != 200):
               print(response.status_code)

        response_order_refresh = self.client.post(url="/api/v1/orderservice/order/refresh", headers=head, json={"loginId": self.user_id,"enableStateQuery":"false","enableTravelDateQuery":"false","enableBoughtDateQuery":"false","travelDateStart":"null","travelDateEnd":"null","boughtDateStart":"null","boughtDateEnd":"null"})
        
        print(json.loads(response_order_refresh.content))  
        response_as_json_order_id = json.loads(response_order_refresh.content)["data"][0]["id"]
        self.order_id = response_as_json_order_id

        response_payment_ticket = self.client.post(url="/api/v1/inside_pay_service/inside_payment", headers=head, json={"orderId": response_as_json_order_id,"tripId":"D1345"})


        


class UserBooking(HttpUser):

    
    wait_time = between(10, 20)



    @task
    def index(self):
        print("user_booking")

        authentication(self)
        purchaseTicket(self)

        response_ticket_collect_refresh = self.client.post(url="/api/v1/orderservice/order/refresh", headers=head, json={"loginId": self.user_id,"enableStateQuery":"false","enableTravelDateQuery":"false","enableBoughtDateQuery":"false","travelDateStart":"null","travelDateEnd":"null","boughtDateStart":"null","boughtDateEnd":"null"})


        response_as_json_ticket_collect_id = json.loads(response_order_refresh.content)["data"][0]["id"]

        response_as_json_collect = self.client.get(url="/api/v1/executeservice/execute/collected/" + response_as_json_ticket_collect_id, headers=head)

        response_as_json_execute = self.client.get(url="/api/v1/executeservice/execute/execute/" + response_as_json_ticket_collect_id, headers=head)


        

   




class UserRoundTripNoLogin(HttpUser):

    
    wait_time = between(10, 20)

    @task
    def index(self):
        print("user_roundtrip_nologin")


        self.client.get('/index.html')
        
        departure_date = "2020-07-27"
        return_date = "2020-07-29"

        head = {"Accept": "application/json", "Content-Type":"application/json"}
        body_start = {
            "startingPlace": "Shang Hai", 
            "endPlace": "Su Zhou",
            "departureTime": departure_date
            }
        body_return = {
            "startingPlace": "Su Zhou",
            "endPlace": "Shang Hai",
            "departureTime": return_date
        }

        with self.client.post(
            url="/api/v1/travelservice/trips/left", 
            headers=head, 
            json=body_start, 
            catch_response=True) as response:
            if response.status_code != 200:
                print(response.status_code)

        with self.client.post(
            url="/api/v1/travelservice/trips/left",
            headers=head, 
            json=body_return, 
            catch_response=True) as response:
            if response.status_code != 200:
                print(response.status_code)



class UserRefundVoucher(HttpUser):


    wait_time= between(10,20)

    @task
    def index(self):
        print("user_refund")

        authentication(self)
        purchaseTicket(self)

        head = {"Accept": "application/json", "Content-Type":"application/json","Authorization": self.bearer}
        
        self.client.post(url="api/v1/orderservice/order/refresh", headers=head)
        

        response_get_voucher = self.client.post(url="/getVoucher", headers=head, json={"orderId":self.order_id,"type":1})

        print("response_voucher")
        print(response_get_voucher.text)

class UserCancelNoRefund(HttpUser):
    wait_time= between(10,20)

    @task
    def index(self):
        print("user_cancel_no_refund")

        authentication(self)
        purchaseTicket(self)

        head = {"Accept": "application/json", "Content-Type":"application/json","Authorization": self.bearer}
        self.client.get(url="/api/v1/cancelservice/cancel/refound/" + self.order_id + "/" + self.user_id, headers=head)

class UserConsignTicket(HttpUser):
    wait_time= between(10,20)

    @task
    def index(self):

        print("user_consign_ticket")

        authentication(self)
        purchaseTicket(self)

        head = {"Accept": "application/json", "Content-Type":"application/json","Authorization": self.bearer}

        self.client.get(url="/api/v1/consignservice/consigns/order/" + self.order_id)

        response_as_json_consign = self.client.put(url="/api/v1/consignservice/consigns", json={"accountId": self.user_id,"handleDate":"2020-07-27","from":"Shang Hai","to":"Su Zhou","orderId":self.order_id,"consignee": self.order_id,"phone":"123","weight":"1","id":"","isWithin":"false"}, headers=head)
        print(response_as_json_consign.text)


class AdminUpdateStayTime(HttpUser):

    wait_time= between(10,20)

    @task
    def index(self):

        print("admin_update_stay_time")
        response1 = self.client.post(url="/api/v1/users/login", json={"username": "admin", "password": "222222"})
        response_as_json1 = json.loads(response1.content)["data"]
        token = response_as_json1["token"]
        beareradmin = "Bearer " + token
        userrID = response_as_json1["userId"]

        head = {"Accept": "application/json", "Content-Type":"application/json","Authorization": beareradmin}

        print("response_allStations")
        response_allStations = self.client.get(url="/api/v1/stationservice/stations", headers = head)


        response_as_json_allStations = json.loads(response_allStations.content)["data"]

        print(response_as_json_allStations)

        

        station = random.choice(response_as_json_allStations)

        station_id = station["id"]
        station_name = station["name"]


        response_as_json_updateStayTime = self.client.put(url="/api/v1/stationservice/stations", json={"id":station_id,"name":"station_name","stayTime":random.randint(10,100)}, headers = head)

        print(response_as_json_updateStayTime.text)
        
        

        

