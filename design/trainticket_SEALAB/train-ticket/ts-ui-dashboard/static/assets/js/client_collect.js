/**
 * Created by ldw on 20178/7/17.
 */
var collectTicket = new Vue({
        el: '#collectTicket',
        data: {
            collect_order_id: ''
        },
        methods: {
            initPage() {
                this.checkLogin();
            },
            checkLogin(){
                var username = sessionStorage.getItem("client_name");
                if (username == null) {
                    // alert("Please login first!");
                }
                else {
                    document.getElementById("client_name").innerHTML = username;
                }
            },
            collectTicket() {
                if (this.collect_order_id != '' && this.collect_order_id != "") {
                    $("#reserve_collect_button").attr("disabled", true);
                    var executeInfo = new Object();
                    executeInfo.orderId = this.collect_order_id;
                    var data = JSON.stringify(executeInfo);
                    $.ajax({
                        type: "post",
                        url: "/execute/collected",
                        contentType: "application/json",
                        dataType: "json",
                        data: data,
                        xhrFields: {
                            withCredentials: true
                        },
                        success: function (result) {
                            var obj = result;
                            if (obj["status"] == true) {
                                alert(obj["message"] + " - you can enter station with your order id !");
                            } else {
                                alert(obj["message"]);
                            }
                        },
                        complete: function () {
                            $("#reserve_collect_button").attr("disabled", false);
                        }
                    });
                } else {
                    alert("please input your order id first !")
                }
            }
        },
        mounted() {
            this.initPage();
        }
    });