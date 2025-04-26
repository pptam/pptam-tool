var stationModule = angular.module("myApp",[]);

stationModule.factory('loadDataService', function ($http, $q) {

    var service = {};

    service.loadAdminBasic = function(url){
        var deferred = $q.defer();
        var promise = deferred.promise;
        //返回的数据对象
        var information = new Object();

        $http({
            method: "get",
            url: url + "/" + sessionStorage.getItem("admin_id"),
            withCredentials: true
        }).success(function (data, status, headers, config) {
            if (data.status) {
                information = data;
                deferred.resolve(information);
            }
            else{
                alert("Request the station list fail!" + data.message);
            }
        });
        return promise;
    };

    return service;
});

stationModule.controller("stationCtrl", function ($scope,$http, loadDataService, $window) {

    //首次加载显示数据
    loadDataService.loadAdminBasic("/adminbasic/getAllStations").then(function (result) {
        // console.log(result);
        $scope.stations = result.stationList;
    });

    $scope.deleteStation = function(station) {
        $('#delete-station-confirm').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                $http({
                    method:"post",
                    url: "/adminbasic/deleteStation",
                    withCredentials: true,
                    data:{
                        loginId:sessionStorage.getItem("admin_id"),
                        id:station.id,
                        name:station.name,
                        stayTime:station.stayTime
                    }
                }).success(function(data, status, headers, config){
                    if (data) {
                       alert("Delete station successfully!");
                    }else{
                        alert("Update station failed!");
                    }
                    $window.location.reload();
                })
            },
            // closeOnConfirm: false,
            onCancel: function () {

            }
        });
    };

    $scope.updateStation = function(station) {
        $('#update-station-name').val(station.name);
        $('#update-station-stay-time').val(station.stayTime);


        $('#update-station-table').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                if(parseInt( $('#update-station-stay-time').val())){
                    var data = new Object();
                    data.id = station.id;
                    data.name =  $('#update-station-name').val();
                    data.stayTime =  parseInt($('#update-station-stay-time').val());
                    data.loginId=sessionStorage.getItem("admin_id");
                    // alert(JSON.stringify(data));
                    $http({
                        method:"post",
                        url: "/adminbasic/modifyStation",
                        withCredentials: true,
                        data:data
                    }).success(function(data, status, headers, config){
                        if (data) {
                            alert("Update station successfully!");
                        }else{
                            alert("Update station failed!");
                        }
                        $window.location.reload();
                    })
                } else {
                    alert("The stay time must be an integer!");
                }

            },
            onCancel: function () {

            }
        });
    };

    $scope.addStation = function() {
        $('#add-station-id').val("");
        $('#add-station-name').val("");
        $('#add-station-stay-time').val("");

        $('#add-station-table').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                if(parseInt( $('#add-station-stay-time').val())){
                    var data = new Object();
                    data.id = $('#add-station-id').val();
                    data.name =  $('#add-station-name').val();
                    data.stayTime =  parseInt($('#add-station-stay-time').val());
                    data.loginId=sessionStorage.getItem("admin_id");
                    // alert(JSON.stringify(data));
                    $http({
                        method:"post",
                        url: "/adminbasic/addStation",
                        withCredentials: true,
                        data:data
                    }).success(function(data, status, headers, config){
                        if (data) {
                            alert("Add station successfully!");
                        }else{
                            alert("Add station failed!");
                        }
                        $window.location.reload();
                    })
                } else{
                    alert("The staytime must be an integer!");
                }

            },
            onCancel: function () {

            }
        });
    };



});