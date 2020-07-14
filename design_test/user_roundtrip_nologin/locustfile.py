from locust import HttpUser, task, between
from datetime import datetime, timedelta, date
from random import randint

#
# In this case, the user will just search for a roundtrip 
# ticket from the website without logging in.
# The departure date will be today's date and the return date is
# generated randomly (from 1 to 10 days) adding it to the departure date. 
# There will be 2 POST requests with two different bodies. 
#


class UserRoundTripNoLogin(HttpUser):
    
    wait_time = between(10, 20)

    @task
    def index(self):
        departure_date = datetime.today().strftime('%Y-%m-%d')
        days = randint(1, 10)
        return_date = datetime.today() + timedelta(days=days)
        return_date = return_date.strftime('%Y-%m-%d')

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
            print(response.text)

        with self.client.post(
            url="/api/v1/travelservice/trips/left",
            headers=head, 
            json=body_return, 
            catch_response=True) as response:
            if response.status_code != 200:
                print(response.status_code)
            print(response.text)
