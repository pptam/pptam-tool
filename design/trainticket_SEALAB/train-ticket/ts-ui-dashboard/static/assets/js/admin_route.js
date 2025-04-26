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
            url: "/adminroute/findAll/" + param.id,
            withCredentials: true,
        }).success(function (data, status, headers, config) {
            if (data.status) {
                information.routeRecords = data.routes;
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
        $scope.records = result.routeRecords;
        //$scope.decodeInfo(result.orderRecords[0]);
    });

    $scope.decodeInfo = function (obj) {
        var des = "";
        for(var name in obj){
            des += name + ":" + obj[name] + ";";
        }
        alert(des);
    }
    
    //Add new route
    $scope.addNewRoute = function () {
        $('#add_prompt').modal({
            relatedTarget: this,
            onConfirm: function(e) {
                $http({
                    method: "post",
                    url: "/adminroute/createAndModifyRoute",
                    withCredentials: true,
                    data:{
                        loginId: sessionStorage.getItem("admin_id"),
                        stationList: $scope.add_route_stations,
                        distanceList: $scope.add_route_distances,
                        startStation: $scope.add_route_start_station,
                        endStation: $scope.add_route_terminal_station
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
    
    //Update exist route
    $scope.updateRoute = function (record) {
        $scope.update_route_id = record.id;
        $scope.update_route_stations = record.stations;
        $scope.update_route_distances = record.distances;
        $scope.update_route_start_station = record.startStationId;
        $scope.update_route_terminal_station = record.terminalStationId;

        $('#update_prompt').modal({
            relatedTarget: this,
            onConfirm: function(e) {
                $http({
                    method: "post",
                    url: "/adminroute/createAndModifyRoute",
                    withCredentials: true,
                    data:{
                        loginId: sessionStorage.getItem("admin_id"),
                        id: $scope.update_route_id,
                        stationList: $scope.update_route_stations + "",
                        distanceList: $scope.update_route_distances + "",
                        startStation: $scope.update_route_start_station,
                        endStation: $scope.update_route_terminal_station
                    }
                }).success(function (data, status, headers, config) {
                    if (data.status) {
                        alert(data.message);
                        $scope.reloadRoute();
                    }
                    else{
                        alert("Update the route fail!" + data.message);
                    }
                });
            },
            onCancel: function(e) {
                alert('You have canceled the operation!');
            }
        });
    }

    //Delete route
    $scope.deleteRoute = function(routeId){
        $('#delete_confirm').modal({
            relatedTarget: this,
            onConfirm: function(options) {
                $http({
                    method: "post",
                    url: "/adminroute/deleteRoute",
                    withCredentials: true,
                    data: {
                        loginId: sessionStorage.getItem("admin_id"),
                        routeId: routeId
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