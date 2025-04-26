/**
 * Created by lwh on 2017/11/16.
 */
/*
 * 显示管理员名字
 * */
var loadBody = function () {
    var username = sessionStorage.getItem("admin_name");
    if (username == null) {
        alert("Please login first!");
        location.href = "adminlogin.html";
    }
    else {
        document.getElementById("admin_name").innerHTML = username;
    }
};

/*
 * 登出
 * */
var logout = function () {
    sessionStorage.clear();
    location.href = "adminlogin.html";
}

/*
 * 将加载数据封装为一个服务
 * */
var app = angular.module('myApp', []);
app.factory('loadDataService', function ($http, $q) {

    var service = {};

    //获取并返回数据
    service.loadRecordList = function (param) {
        var deferred = $q.defer();
        var promise = deferred.promise;
        //返回的数据对象
        var information = new Object();

        $http({
            method: "get",
            url: "/adminuser/findAll/" + param.id,
            withCredentials: true,
        }).success(function (data, status, headers, config) {
            if (data.status) {
                information.userRecords = data.accountArrayList;
                deferred.resolve(information);
            }
            else{
                alert("Request the order list fail!" + data.message);
            }
        });

        return promise;
    };

    return service;
});

/*
 * 加载列表
 * */
app.controller('indexCtrl', function ($scope, $http,$window,loadDataService) {
    var param = {};
    param.id = sessionStorage.getItem("admin_id");

    //刷新页面
    $scope.reloadRoute = function () {
        $window.location.reload();
    };

    //首次加载显示数据
    loadDataService.loadRecordList(param).then(function (result) {
        $scope.records = result.userRecords;
        //$scope.decodeInfo(result.orderRecords[0]);
    });

    $scope.decodeInfo = function (obj) {
        var des = "";
        for(var name in obj){
            des += name + ":" + obj[name] + ";";
        }
        alert(des);
    }
    
    //Add new user
    $scope.addNewUser = function () {
        $('#add_prompt').modal({
            relatedTarget: this,
            onConfirm: function(e) {
                $http({
                    method: "post",
                    url: "/adminuser/addUser",
                    withCredentials: true,
                    data:{
                        loginId: sessionStorage.getItem("admin_id"),
                        name: $scope.add_user_name,
                        password: $scope.add_user_password,
                        gender: $scope.add_user_gender,
                        email: $scope.add_user_email,
                        documentType: $scope.add_user_document_type,
                        documentNum: $scope.add_user_document_number
                    }
                }).success(function (data, status, headers, config) {
                    if (data.status) {
                        alert(data.message);
                        $scope.reloadRoute();
                    }
                    else{
                        alert("Add the route fail!" + data.message);
                    }
                });
            },
            onCancel: function(e) {
                alert('You have canceled the operation!');
            }
        });
    }
    
    //Update exist user
    $scope.updateUser = function (record) {
        $scope.update_user_id = record.id;
        $scope.update_user_name = record.name;
        $scope.update_user_password = record.password;
        $scope.update_user_gender = record.gender;
        $scope.update_user_email = record.email;
        $scope.update_user_document_type = record.documentType;
        $scope.update_user_document_number = record.documentNum;

        $('#update_prompt').modal({
            relatedTarget: this,
            onConfirm: function(e) {
                $http({
                    method: "post",
                    url: "/adminuser/updateUser",
                    withCredentials: true,
                    data:{
                        loginId: sessionStorage.getItem("admin_id"),
                        modifyAccountInfo:{
                            accountId: $scope.update_user_id,
                            newName: $scope.update_user_name,
                            newPassword: $scope.update_user_password,
                            newGender: $scope.update_user_gender,
                            newEmail: $scope.update_user_email,
                            newDocumentType: $scope.update_user_document_type,
                            newDocumentNumber: $scope.update_user_document_number
                        }
                    }
                }).success(function (data, status, headers, config) {
                    if (data.status) {
                        alert(data.message);
                        $scope.reloadRoute();
                    }
                    else{
                        alert("Update the user fail!" + data.message);
                    }
                });
            },
            onCancel: function(e) {
                alert('You have canceled the operation!');
            }
        });
    }

    //Delete user
    $scope.deleteUser = function(accountId){
        $('#delete_confirm').modal({
            relatedTarget: this,
            onConfirm: function(options) {
                $http({
                    method: "post",
                    url: "/adminuser/deleteUser",
                    withCredentials: true,
                    data: {
                        loginId: sessionStorage.getItem("admin_id"),
                        accountId: accountId
                    }
                }).success(function (data, status, headers, config) {
                    if (data.status) {
                        alert(data.message);
                        $scope.reloadRoute();
                    }
                    else{
                        alert("Delete the route fail!" + data.message);
                    }
                });
            },
            // closeOnConfirm: false,
            onCancel: function() {
                alert('You have canceled the operation!');
            }
        });
    }
});