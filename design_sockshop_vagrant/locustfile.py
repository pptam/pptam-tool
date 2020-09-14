# This file describes the test execution. It is based on a previous version, developed for Faban (http://faban.org), which,
# for documentation reasons, is attached at the bottom of this file.

import random
import json
import datetime
import secrets
from locust import HttpUser, task, between
import requests


def get_home(self):
    self.client.get("/index.html", verify=False)


def get_login(self):
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


def get_address(self):
    self.client.get("/address", verify=False)


def perform_operation(self, name):
    all_operations = {"home": get_home, "login": get_login, "getCatalogue": get_catalog_variant_1, "catalogueSize": get_catalog_variant_2, "cataloguePage": get_catalog_variant_3, "catalogue": get_category, "getItem": get_item, "getRelated": get_related, "showDetails": get_details, "tags": get_tags, "getCart": get_cart, "addToCart": add_to_cart, "basket": get_basket, "createOrder": get_orders, "getOrders": get_orders, "viewOrdersPage": get_all_orders, "getCustomer": get_customer, "getCard": get_card, "getAddress": get_address}
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


# package pptam.driver;

# import com.sun.faban.driver.*;
# import com.sun.faban.driver.util.Random;
# import com.sun.faban.driver.util.ContentSizeStats;

# import javax.xml.xpath.XPathExpressionException;
# import java.io.IOException;
# import java.util.logging.Logger;
# import java.util.HashMap;
# import java.util.Map;

# /**
#  * Simple web driver example.
#  */
# @BenchmarkDefinition(name = "PPTAM-${TEST_NAME}", version = "0.2")
# @BenchmarkDriver(name = "WebDriver", threadPerScale = 1)
# // # Visitor: View Home -> View Catalogue -> View Details
# // - [ home, getCatalogue, getCart, home, getCatalogue, getCart, catalogue,
# // catalogueSize, tags, cataloguePage, getCart, getCustomer, showDetails,
# // getItem, getCustomer, getCart, getRelated ]
# // # Buyer: View Home -> Login -> View Catalogue -> View Details -> Add to Cart
# // -> View Cart -> Create order
# // - [ home, getCatalogue, getCart, login, home, getCatalogue, getCart, home,
# // getCatalogue, getCart, catalogue, catalogueSize, tags, cataloguePage,
# // getCart, getCustomer, showDetails, getItem, getCustomer, getCart, getRelated,
# // addToCart, showDetails, getItem, getCustomer, getCart, getRelated, basket,
# // getCart, getCard, getAddress, getCatalogue, getItem, getCart, getCustomer,
# // getItem, createOrder, viewOrdersPage, getOrders, getCart, getCustomer,
# // getItem ]
# // # Orders visitor: View Home -> Login -> View orders
# // - [ home, getCatalogue, getCart, login, home, getCatalogue, getCart,
# // viewOrdersPage, getOrders, getCart, getCustomer, getItem ]
# @FlatSequenceMix(mix = { 40, 30, 30 }, sequences = {
#         @OperationSequence({ "home", "getCatalogue", "getCart", "home", "getCatalogue", "getCart", "catalogue",
#                 "catalogueSize", "tags", "cataloguePage", "getCart", "getCustomer", "showDetails", "getItem",
#                 "getCustomer", "getCart", "getRelated" }),
#         @OperationSequence({ "home", "getCatalogue", "getCart", "login", "home", "getCatalogue", "getCart", "home",
#                 "getCatalogue", "getCart", "catalogue", "catalogueSize", "tags", "cataloguePage", "getCart",
#                 "getCustomer", "showDetails", "getItem", "getCustomer", "getCart", "getRelated", "addToCart",
#                 "showDetails", "getItem", "getCustomer", "getCart", "getRelated", "basket", "getCart", "getCard",
#                 "getAddress", "getCatalogue", "getItem", "getCart", "getCustomer", "getItem", "createOrder",
#                 "viewOrdersPage", "getOrders", "getCart", "getCustomer", "getItem" }),
#         @OperationSequence({ "home", "getCatalogue", "getCart", "login", "home", "getCatalogue", "getCart",
#                 "viewOrdersPage", "getOrders", "getCart", "getCustomer", "getItem" }) }, deviation = 5)
# // @NegativeExponential (
# // cycleType = CycleType.THINKTIME,
# // cycleDeviation = 5
# // )
# public class WebDriver {

#     /** The driver context for this instance. */
#     private DriverContext ctx;
#     private HttpTransport http;
#     private String home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem, getRelated, showDetails,
#             tags, getCart, addToCart, basket, createOrder, getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     Logger logger;
#     Random random;

#     /**
#      * Constructs the web driver.
#      *
#      * @throws XPathExpressionException An XPath error occurred
#      */
#     public WebDriver() throws XPathExpressionException {
#         ctx = DriverContext.getContext();
#         HttpTransport.setProvider("com.sun.faban.driver.transport.hc3.ApacheHC3Transport");
#         http = HttpTransport.newInstance();
#         logger = ctx.getLogger();
#         random = ctx.getRandom();
#         String host = ctx.getXPathValue("/webBenchmark${TEST_NAME}/serverConfig/host");
#         String port = ctx.getXPathValue("/webBenchmark${TEST_NAME}/serverConfig/port");

#         String basepath = "http://" + host + ":" + port;

#         home = basepath + "/index.html";
#         login = basepath + "/login";
#         getCatalogue = basepath + "/catalogue?size=5";
#         catalogueSize = basepath + "/catalogue/size";
#         cataloguePage = basepath + "/catalogue?page=1&size=6";
#         catalogue = basepath + "/category.html";
#         getItem = basepath + "/catalogue/3395a43e-2d88-40de-b95f-e00e1502085b";
#         getRelated = basepath + "/catalogue?sort=id&size=3&tags=brown";
#         showDetails = basepath + "/detail.html?id=3395a43e-2d88-40de-b95f-e00e1502085b";
#         tags = basepath + "/tags";
#         getCart = basepath + "/cart";
#         addToCart = basepath + "/cart";
#         basket = basepath + "/basket.html";
#         createOrder = basepath + "/orders";
#         getOrders = basepath + "/orders";
#         viewOrdersPage = basepath + "/customer-orders.html";
#         getCustomer = basepath + "/customers/fz5cpW831_cB4MMSsuphqSgPw7XHYHa0";
#         getCard = basepath + "/card";
#         getAddress = basepath + "/address";
#     }

#     /**
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "home", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doHome() throws IOException {
#         logger.finest("Accessing " + home);
#         http.fetchURL(home);
#     }

#     /**
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "login", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doLogin() throws IOException {
#         logger.finest("Accessing " + login);
#         Map<String, String> headers = new HashMap<String, String>();
#         headers.put("Authorization", "Basic dXNlcjpwYXNzd29yZA==");
#         http.readURL(login, headers);
#     }

#     /**
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "getCatalogue", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doGetCatalogue() throws IOException {
#         logger.finest("Accessing " + getCatalogue);
#         http.fetchURL(getCatalogue);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "catalogueSize", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doCatalogueSize() throws IOException {
#         logger.finest("Accessing " + catalogueSize);
#         http.fetchURL(catalogueSize);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "cataloguePage", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doCataloguePage() throws IOException {
#         logger.finest("Accessing " + cataloguePage);
#         http.fetchURL(cataloguePage);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "catalogue", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doCatalogue() throws IOException {
#         logger.finest("Accessing " + catalogue);
#         Map<String, String> headers = new HashMap<String, String>();
#         headers.put("Content-Type", "html");
#         http.readURL(catalogue, headers);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "getItem", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doGetItem() throws IOException {
#         logger.finest("Accessing " + getItem);
#         http.fetchURL(getItem);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "getRelated", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doGetRelated() throws IOException {
#         logger.finest("Accessing " + getRelated);
#         http.fetchURL(getRelated);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "showDetails", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doShowDetails() throws IOException {
#         logger.finest("Accessing " + showDetails);
#         Map<String, String> headers = new HashMap<String, String>();
#         headers.put("Content-Type", "html");
#         http.readURL(showDetails, headers);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "tags", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doTags() throws IOException {
#         logger.finest("Accessing " + tags);
#         http.fetchURL(tags);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "getCart", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doGetCart() throws IOException {
#         logger.finest("Accessing " + getCart);
#         http.fetchURL(getCart);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "addToCart", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doAddToCart() throws IOException {
#         logger.finest("Accessing " + addToCart);
#         Map<String, String> headers = new HashMap<String, String>();
#         headers.put("Content-Type", "application/json");
#         String post = "\"{id: '3395a43e-2d88-40de-b95f-e00e1502085b'}\"";
#         http.fetchURL(addToCart, post, headers);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "basket", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doBasket() throws IOException {
#         logger.finest("Accessing " + basket);
#         Map<String, String> headers = new HashMap<String, String>();
#         headers.put("Content-Type", "application/json");
#         http.readURL(basket, headers);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "createOrder", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doCreateOrder() throws IOException {
#         logger.finest("Accessing " + createOrder);
#         http.fetchURL(createOrder);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "getOrders", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doGetOrders() throws IOException {
#         logger.finest("Accessing " + getOrders);
#         http.fetchURL(getOrders);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "viewOrdersPage", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doViewOrdersPage() throws IOException {
#         logger.finest("Accessing " + viewOrdersPage);
#         http.fetchURL(viewOrdersPage);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "getCustomer", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doGetCustomer() throws IOException {
#         logger.finest("Accessing " + getCustomer);
#         http.fetchURL(getCustomer);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "getCard", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doGetCard() throws IOException {
#         logger.finest("Accessing " + getCard);
#         http.fetchURL(getCard);
#     }

#     // home, login, getCatalogue, catalogueSize, cataloguePage, catalogue, getItem,
#     // getRelated, showDetails, tags, getCart, addToCart, basket, createOrder,
#     // getOrders, viewOrdersPage, getCustomer, getCard, getAddress;
#     /**
#      * First operation.
#      *
#      * @throws IOException An I/O or network error occurred.
#      */
#     @BenchmarkOperation(name = "getAddress", max90th = 20, timing = Timing.AUTO)
#     @NegativeExponential(cycleType = CycleType.THINKTIME, cycleDeviation = 5)
#     public void doGetAddress() throws IOException {
#         logger.finest("Accessing " + getAddress);
#         http.fetchURL(getAddress);
#     }

# }
