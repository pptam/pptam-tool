
var loginApp = new Vue({
    el: '#loginApp',
    data:{
        email: 'fdse_microservices@163.com',
        password: 'DefaultPassword',
        verifiCode: '1234'
    },
    methods: {
        initPage () {
            this.checkIfLogin();
        },
        checkIfLogin(){
            var username = sessionStorage.getItem("client_name");
            if (username == null) {
                alert("Please login first!");
            }
            else {
                document.getElementById("client_name").innerHTML = username;
            }
        },
        login () {
            var loginInfo = new Object();
            loginInfo.email = this.email;
            if(loginInfo.email == null || loginInfo.email == ""){
                alert("Email Can Not Be Empty.");
                return;
            }
            if(this.checkEmailFormat(loginInfo.email) == false){
                alert("Email Format Wrong.");
                return;
            }
            loginInfo.password = this.password;
            if(loginInfo.password == null || loginInfo.password == ""){
                alert("Password Can Not Be Empty.");
                return;
            }
            loginInfo.verificationCode = this.verifiCode;
            if(loginInfo.verificationCode == null || loginInfo.verificationCode == ""){
                alert("Verification Code Can Not Be Empty.");
                return;
            }
            var data = JSON.stringify(loginInfo);
            $.ajax({
                type: "post",
                url: "/login",
                contentType: "application/json",
                dataType: "json",
                data:data,
                xhrFields: {
                    withCredentials: true
                },
                success: function(result){
                    var obj = result;
                    if(obj["status"] == true){
                        sessionStorage.setItem("client_id",obj["account"].id);
                        sessionStorage.setItem("client_name", obj["account"].name);
                        document.cookie = "loginId=" + obj["account"].id;
                        document.cookie = "loginToken=" + obj["token"];
                        document.getElementById("client_name").innerHTML = obj["account"].name;
                        //  alert(obj["message"] + obj["account"].name + "======-");
                        // login in success
                        $("#flow_preserve_login_status").text(obj["status"]);
                        $("#flow_preserve_login_msg").text(obj["message"]);
                    }else{
                        setCookie("loginId", "", -1);
                        setCookie("loginToken", "", -1);
                        // alert(obj["message"]);
                        sessionStorage.setItem("client_id","-1");
                        sessionStorage.setItem("client_name", "Not Login");
                        document.getElementById("client_name").innerHTML = "Not Login";

                        $("#flow_preserve_login_msg").text(obj["message"]);
                    }
                }
            });
        },
        checkEmailFormat(email){
            var emailFormat = /^([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+@([a-zA-Z0-9]+[_|\_|\.]?)*[a-zA-Z0-9]+\.[a-zA-Z]{2,3}$/;
            if(!emailFormat.test(email)){
                return false;
            }else{
                return true;
            }
        }
    },
    mounted () {
        this.initPage();
    }
});