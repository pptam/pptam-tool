from locust import HttpUser, task, between


class UserTripNoLogin(HttpUser):
    wait_time = between(10, 20)

    @task
    def index(self):
        body = {"startingPlace": "Shang Hai", "endPlace": "Su Zhou", "departureTime": "2020-07-14"}
        with self.client.post("/api/v1/travelservice/trips/left", body, catch_response=True) as response:
            if response.status_code != "200":
                print(response.status_code)
