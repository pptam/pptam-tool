var appConsign = new Vue({
    el: '#vueConsignApp',
    data: {
        myConsigns: []
    },
    methods: {
        queryMyConsign() {
            var accountid = getCookie("loginId");
            var that = this;
            $.ajax({
                type: "get",
                url: "/consign/findByAccountId/" + accountid,
                dataType: "json",
                xhrFields: {
                    withCredentials: true
                },
                success: function (result) {
                    var size = result.length;
                    that.myConsigns =  new Array(size);
                    for (var i = 0; i < size; i++) {
                        that.myConsigns[i]  = result[i];
                      // that.myConsigns[i].from = that.getStationNameById(that.myConsigns[i].from);
                      // that.myConsigns[i].to = that.getStationNameById(that.myConsigns[i].to);
                      //  that.myConsigns[i].handleDate = that.convertNumberToDateTimeString(that.myConsigns[i].handleDate);
                        that.myConsigns[i].targetDate = that.convertNumberToDateTimeString(that.myConsigns[i].targetDate);
                    }
                }
            });

        },
        logOutClient (){
            var logoutInfo = new Object();
            logoutInfo.id = this.getCookie("loginId");
            if(logoutInfo.id == null || logoutInfo.id == ""){
                alert("No cookie named 'loginId' exist. please login");
                location.href = "client_login.html";
                return;
            }
            logoutInfo.token = this.getCookie("loginToken");
            if(logoutInfo.token == null || logoutInfo.token == ""){
                alert("No cookie named 'loginToken' exist.  please login");
                location.href = "client_login.html";
                return;
            }
            var data = JSON.stringify(logoutInfo);
            var that = this;
            $.ajax({
                type: "post",
                url: "/logout",
                contentType: "application/json",
                dataType: "json",
                data:data,
                xhrFields: {
                    withCredentials: true
                },
                success: function(result){
                    if(result["status"] == true){
                        that.setCookie("loginId", "", -1);
                        that.setCookie("loginToken", "", -1);
                    }else if(result["message"] == "Not Login"){
                        that.setCookie("loginId", "", -1);
                        that.setCookie("loginToken", "", -1);
                    }
                    sessionStorage.setItem("client_id","-1");
                    sessionStorage.setItem("client_name", "Not Login");
                    document.getElementById("client_name").innerHTML = "Not Login";
                    location.href= "client_login.html";
                },
                error: function (e) {
                    alert("logout error");
                }
            });
        },
        getStationNameById(stationId){
            var stationName;
            var getStationInfoOne = new Object();
            getStationInfoOne.stationId =  stationId;
            var getStationInfoOneData = JSON.stringify(getStationInfoOne);
            $.ajax({
                type: "post",
                url: "/station/queryById",
                contentType: "application/json",
                dataType: "json",
                data:getStationInfoOneData,
                async: false,
                xhrFields: {
                    withCredentials: true
                },
                success: function (result) {
                    stationName = result["name"];
                }
            });
            //alert("Return Station Name:" + stationName);
            return stationName;
        },
        convertNumberToDateTimeString(timeNumber){
            var date = new Date(timeNumber);
            return date.toISOString().slice(0,10);
        },
        setCookie(cname, cvalue, exdays) {
            var d = new Date();
            d.setTime(d.getTime() + (exdays*24*60*60*1000));
            var expires = "expires="+d.toUTCString();
            document.cookie = cname + "=" + cvalue + "; " + expires;
        }

    },
    mounted() {
        var username = sessionStorage.getItem("client_name");
        if (username == null || username == "Not Login") {
           // alert("Please login first!");
        }
        else {
            document.getElementById("client_name").innerHTML = username;
            this.queryMyConsign();
        }
    }
});