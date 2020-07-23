from locust import HttpUser, task, between
from datetime import datetime, timedelta, date
from random import randint
import json
#
# In this case, the user will just search for a roundtrip 
# ticket from the website without logging in.
# The departure date will be today's date and the return date is
# generated randomly (from 1 to 10 days) adding it to the departure date. 
# There will be 2 POST requests with two different bodies. 
#


class UserBooking(HttpUser):
    
    wait_time = between(10, 20)
    def on_start(self):
        print("----- on_start")

        # Removes trailing / from the host name to avoid exceptions in the tests
        self.host = self.host.rstrip("/")

        self.client.get('/client_login.html')

        response = self.client.post(url="/api/v1/users/login",
                                    json={
                                        "username": "fdse_microservice",
                                        "password": "111111"
                                    })

        response_as_json = json.loads(response.content)["data"]
        token = response_as_json["token"]
        self.bearer = "Bearer " + token
        self.user_id = response_as_json["userId"]

    @task
    def index(self):

        self.client.get('/index.html')
    	
        departure_date = datetime.today().strftime('%Y-%m-%d')

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
            print(response.text)

        self.client.get(
            url="/client_ticket_book.html?tripId=D1345&from=Shang%20Hai&to=Su%20Zhou&seatType=2&seat_price=50.0&date="+ departure_date,
            headers=head
            )

        self.client.get(url="/api/v1/assuranceservice/assurances/types",headers=head)
        self.client.get(url="/api/v1/foodservice/foods/2020-07-23/Shang%20Hai/Su%20Zhou/D1345", headers=head)

        response = self.client.get(url="/api/v1/contactservice/contacts/account/" + self.user_id, headers=head)

        response_as_json = json.loads(response.content)["data"][0]
        self.contactid = response_as_json["id"]
        

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
            print(response.text)
