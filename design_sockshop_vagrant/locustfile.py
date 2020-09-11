import random
import json
import datetime
import secrets
from locust import HttpUser, task, between
import requests


def get_home(self):
    self.client.get("/index.html", verify=False)


def login(self):
    head = {"Accept": "application/json", "Content-Type": "application/json", "Authorization": "Basic dXNlcjpwYXNzd29yZA=="}
    self.client.get(url="/login", headers=head, verify=False)


def get_catalog_variant_1(self):
    self.client.get("/catalogue?size=5", verify=False)


def get_catalog_variant_2(self):
    self.client.get("/catalogue/size", verify=False)


def get_catalog_variant_3(self):
    self.client.get("/catalogue?page=1&size=6", verify=False)


def get_category(self):
    head = {"Content-Type": "html"}
    self.client.get(url="/category.html", headers=head, verify=False)


def get_item(self):
    self.client.get("/catalogue/3395a43e-2d88-40de-b95f-e00e1502085b", verify=False)


def get_related(self):
    self.client.get("/catalogue?sort=id&size=3&tags=brown", verify=False)


def get_details(self):
    head = {"Content-Type": "html"}
    self.client.get(url="/detail.html?id=3395a43e-2d88-40de-b95f-e00e1502085b", headers=head, verify=False)


def get_tags(self):
    self.client.get("/tags", verify=False)


def get_cart(self):
    self.client.get("/cart", verify=False)


def add_to_cart(self):
    head = {"Content-Type": "application/json"}
    self.client.post(url="/cart", headers=head, json={"id": "3395a43e-2d88-40de-b95f-e00e1502085b"})


def get_basket(self):
    head = {"Content-Type": "application/json"}
    self.client.get(url="/basket.html", headers=head, verify=False)


def get_orders(self):
    self.client.get("/orders", verify=False)


def get_all_orders(self):
    self.client.get("/customer-orders.html", verify=False)


def get_customer(self):
    self.client.get("/customers/fz5cpW831_cB4MMSsuphqSgPw7XHYHa0", verify=False)


def get_card(self):
    self.client.get("/card", verify=False)


def get_adress(self):
    self.client.get("/address", verify=False)


def perform_operation(self, name):
    all_operations = {"home": "get_home", "login": "get_login", "getCatalogue": "get_catalog_variant_1", "catalogueSize": "get_catalog_variant_2", "cataloguePage": "get_catalog_variant_3", "catalogue": "get_category", "getItem": "get_item", "getRelated": "get_related", "showDetails": "get_details", "tags": "get_tags", "getCart": "get_cart", "addToCart": "add_to_cart", "basket": "get_basket", "createOrder": "get_orders", "getOrders": "get_orders", "viewOrdersPage": "get_all_orders", "getCustomer": "get_customer", "getCard": "get_card", "getAddress": "get_address"}
    operation = all_operations.get(name)
    operation(self)


class UserNoLogin(HttpUser):

    @task
    def perform_task(self):
        operations = ["home", "getCatalogue", "getCart", "home", "getCatalogue", "getCart", "catalogue", "catalogueSize", "tags", "cataloguePage", "getCart", "getCustomer", "showDetails", "getItem", "getCustomer", "getCart", "getRelated"]

        for operation in operations:
            perform_operation(self, operation)


class UserLoginAndShop(HttpUser):

    @task
    def perform_task(self):
        operations = ["home", "getCatalogue", "getCart", "login", "home", "getCatalogue", "getCart", "home", "getCatalogue", "getCart", "catalogue", "catalogueSize", "tags", "cataloguePage", "getCart", "getCustomer", "showDetails", "getItem", "getCustomer", "getCart", "getRelated", "addToCart", "showDetails", "getItem", "getCustomer", "getCart", "getRelated", "basket", "getCart", "getCard", "getAddress", "getCatalogue", "getItem", "getCart", "getCustomer", "getItem", "createOrder", "viewOrdersPage", "getOrders", "getCart", "getCustomer", "getItem"]

        for operation in operations:
            perform_operation(self, operation)


class UserLoginAndCheckCart(HttpUser):

    @task
    def perform_task(self):
        operations = ["home", "getCatalogue", "getCart", "login", "home", "getCatalogue", "getCart", "viewOrdersPage", "getOrders", "getCart", "getCustomer", "getItem"]

        for operation in operations:
            perform_operation(self, operation)
