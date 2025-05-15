from locust import HttpUser, task, between, stats
import random
import time

stats.PERCENTILES_TO_REPORT = [0.25, 0.50, 0.75]

class HotelBookingUser(HttpUser):
    wait_time = between(1, 3)  # Simulates real users with random wait times

    def on_start(self):
        """Executed when a simulated user starts"""
        random.seed(time.time())

    def get_user(self):
        """Generate a random user with a consistent username and password"""
        user_id = random.randint(0, 500)
        username = f"Cornell_{user_id}"
        password = str(user_id) * 10  # 10-digit password
        return username, password

    @task(600)  # Scaled from 60
    def search_hotel(self):
        """Simulates a hotel search"""
        in_date = random.randint(9, 23)
        out_date = random.randint(in_date + 1, 24)
        in_date_str = f"2015-04-{in_date:02d}"
        out_date_str = f"2015-04-{out_date:02d}"

        lat = 38.0235 + (random.randint(0, 481) - 240.5) / 1000.0
        lon = -122.095 + (random.randint(0, 325) - 157.0) / 1000.0

        self.client.get(
            f"/hotels?inDate={in_date_str}&outDate={out_date_str}&lat={lat}&lon={lon}",
            name="/hotels",
        )

    @task(390)  # Scaled from 39
    def recommend(self):
        """Simulates requesting a hotel recommendation"""
        req_param = random.choice(["dis", "rate", "price"])
        lat = 38.0235 + (random.randint(0, 481) - 240.5) / 1000.0
        lon = -122.095 + (random.randint(0, 325) - 157.0) / 1000.0

        self.client.get(
            f"/recommendations?require={req_param}&lat={lat}&lon={lon}",
            name="/recommendations",
        )

    @task(5)  # Scaled from 0.5
    def user_login(self):
        """Simulates a user login request with username and password in the URL"""
        username, password = self.get_user()
        
        self.client.post(
            f"/user?username={username}&password={password}",
            name="/login"
        )


    @task(5)  # Scaled from 0.5
    def reserve(self):
        """Simulates a hotel reservation request with parameters in the URL"""
        in_date = random.randint(9, 23)
        out_date = in_date + random.randint(1, 5)

        in_date_str = f"2015-04-{in_date:02d}"
        out_date_str = f"2015-04-{out_date:02d}"

        lat = 38.0235 + (random.randint(0, 481) - 240.5) / 1000.0
        lon = -122.095 + (random.randint(0, 325) - 157.0) / 1000.0

        hotel_id = random.randint(1, 80)
        username, password = self.get_user()
        cust_name = username
        num_room = 1

        self.client.post(
            f"/reservation?inDate={in_date_str}&outDate={out_date_str}"
            f"&lat={lat}&lon={lon}&hotelId={hotel_id}&customerName={cust_name}"
            f"&username={username}&password={password}&number={num_room}",
            name="/reservation"
        )

