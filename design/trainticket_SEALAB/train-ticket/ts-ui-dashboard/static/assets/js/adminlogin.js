/**
 * Created by lwh on 2017/11/16.
 */
var controllerModule = angular.module("myApp", []);
controllerModule.controller("loginCtrl", function ($scope,$http) {
    $scope.login = function() {
        var account = $scope.username;
        var password = $scope.password;
        $http({
            method:"post",
            url: "/account/adminlogin",
            withCredentials: true,
            data:{
                name: account,
                password: password
            }
        }).success(function(data, status, headers, config){
            if (data != null) {
                sessionStorage.setItem("admin_id",data.id);
                sessionStorage.setItem("admin_name", data.name);
                location.href = "../../admin.html";
            }else{
                alert("Wrong user name and password!");
            }
        })
    }

    $scope.decodeInfo = function (obj) {
        var des = "";
        for(var name in obj){
            des += name + ":" + obj[name] + ";";
        }
        alert(des);
    }
});