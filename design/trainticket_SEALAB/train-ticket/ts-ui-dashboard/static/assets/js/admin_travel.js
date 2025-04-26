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
            url: "/admintravel/findAll/" + param.id,
            withCredentials: true,
        }).success(function (data, status, headers, config) {
            if (data.status) {
                information.travelRecords = data.trips;
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
        $scope.records = result.travelRecords;
        //$scope.decodeInfo(result.orderRecords[0]);
    });

    $scope.decodeInfo = function (obj) {
        var des = "";
        for(var name in obj){
            des += name + ":" + obj[name] + ";";
        }
        alert(des);
    }
    
    //Add new travel
    $scope.addNewTravel = function () {
        $('#add_prompt').modal({
            relatedTarget: this,
            onConfirm: function(e) {
                $http({
                    method: "post",
                    url: "/admintravel/addTravel",
                    withCredentials: true,
                    data:{
                        loginId: sessionStorage.getItem("admin_id"),
                        tripId: $scope.add_travel_id,
                        trainTypeId: $scope.add_travel_train_type_id,
                        routeId: $scope.add_travel_route_id,
                        startingTime: $scope.add_travel_start_time
                    }
                }).success(function (data, status, headers, config) {
                    if(data.status){
                        alert(data.message);
                        $scope.reloadRoute();
                    }
                    else{
                        alert(data.message);
                    }
                });
            },
            onCancel: function(e) {
                alert('You have canceled the operation!');
            }
        });
    }
    
    //Update exist travel
    $scope.updateTravel = function (record) {
        $scope.update_travel_id = record.trip.tripId.type + "" + record.trip.tripId.number;
        $scope.update_travel_train_type_id = record.trip.trainTypeId;
        $scope.update_travel_route_id = record.trip.routeId;
        $scope.update_travel_start_time = record.trip.startingTime;

        $('#update_prompt').modal({
            relatedTarget: this,
            onConfirm: function(e) {
                $http({
                    method: "post",
                    url: "/admintravel/updateTravel",
                    withCredentials: true,
                    data:{
                        loginId: sessionStorage.getItem("admin_id"),
                        tripId: $scope.update_travel_id,
                        trainTypeId: $scope.update_travel_train_type_id,
                        routeId: $scope.update_travel_route_id,
                        startingTime: $scope.update_travel_start_time
                    }
                }).success(function (data, status, headers, config) {
                    if(data.status){
                        alert(data.message);
                        $scope.reloadRoute();
                    }
                    else{
                        alert(data.message);
                    }
                });
            },
            onCancel: function(e) {
                alert('You have canceled the operation!');
            }
        });
    }

    //Delete travel
    $scope.deleteTravel = function(travelId){
        var tripId = travelId.type + "" + travelId.number;
        $('#delete_confirm').modal({
            relatedTarget: this,
            onConfirm: function(options) {
                $http({
                    method: "post",
                    url: "/admintravel/deleteTravel",
                    withCredentials: true,
                    data: {
                        loginId: sessionStorage.getItem("admin_id"),
                        tripId: tripId
                    }
                }).success(function (data, status, headers, config) {
                    if(data.status){
                        alert(data.message);
                        $scope.reloadRoute();
                    }
                    else{
                        alert(data.message);
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