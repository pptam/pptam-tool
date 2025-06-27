from locust import HttpUser, task, between

class ChineseStyleUser(HttpUser):
    # wait_time = between(5, 9)

    @task
    def see_news(self):
        self.client.get("/")
        self.client.get("/world/china")

    @task
    def see_style(self):
        self.client.get("/")
        self.client.get("/style")

class ItalianArchitectUser(HttpUser):

    @task
    def see_offers(self):
        self.client.get("/")
        self.client.get("/world/europe")
        self.client.get("/style/architecture")
