

$("#logout_button").click(function() {
    var logoutInfo = new Object();
    logoutInfo.id = getCookie("loginId");
    if(logoutInfo.id == null || logoutInfo.id == ""){
        alert("No cookie named 'loginId' exist. please login");
        location.href = "client_login.html";
        return;
    }
    logoutInfo.token = getCookie("loginToken");
    if(logoutInfo.token == null || logoutInfo.token == ""){
        alert("No cookie named 'loginToken' exist.  please login");
        location.href = "client_login.html";
        return;
    }
    var data = JSON.stringify(logoutInfo);
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
                setCookie("loginId", "", -1);
                setCookie("loginToken", "", -1);
            }else if(result["message"] == "Not Login"){
                setCookie("loginId", "", -1);
                setCookie("loginToken", "", -1);
            }
            sessionStorage.setItem("client_id","-1");
            sessionStorage.setItem("client_name", "Not Login");
            document.getElementById("client_name").innerHTML = "Not Login";
            location.href= "client_login.html";
            alert("logout success!")
        },
        error: function (e) {
            alert("logout error");
        }
    });
});

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays*24*60*60*1000));
    var expires = "expires="+d.toUTCString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i< ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name)==0)
            return c.substring(name.length,c.length);
    }
    return "";
}