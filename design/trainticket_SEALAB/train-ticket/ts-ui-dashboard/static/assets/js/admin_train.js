var trainModule = angular.module("myApp",[]);

trainModule.factory('loadDataService', function ($http, $q) {

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
                alert("Request the train list fail!" + data.message);
            }
        });
        return promise;
    };

    return service;
});

trainModule.controller("trainCtrl", function ($scope,$http, loadDataService, $window) {

    //首次加载显示数据
    loadDataService.loadAdminBasic("/adminbasic/getAllTrains").then(function (result) {
        // console.log(result);
        $scope.trains = result.trainList;
    });

    $scope.deleteTrain = function(train) {
        $('#delete-train-confirm').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                $http({
                    method:"post",
                    url: "/adminbasic/deleteTrain",
                    withCredentials: true,
                    data:{
                        loginId:sessionStorage.getItem("admin_id"),
                        id:train.id,
                        economyClass:train.economyClass,
                        confortClass:train.confortClass,
                        averageSpeed:train.averageSpeed
                    }
                }).success(function(data, status, headers, config){
                    if (data) {
                       alert("Delete train successfully!");
                    }else{
                        alert("Update train failed!");
                    }
                    $window.location.reload();
                })
            },
            // closeOnConfirm: false,
            onCancel: function () {

            }
        });
    };

    $scope.updateTrain = function(train) {
        $('#update-train-id').val(train.id);
        $('#update-train-economy-class').val(train.economyClass);
        $('#update-train-confort-class').val(train.confortClass);
        $('#update-train-average-speed').val(train.averageSpeed);

        $('#update-train-table').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                if(parseInt( $('#update-train-economy-class').val()) && parseInt( $('#update-train-confort-class').val()) && parseInt( $('#update-train-average-speed').val())){
                    var data = new Object();
                    data.id = train.id;
                    data.economyClass = parseInt( $('#update-train-economy-class').val());
                    data.confortClass = parseInt( $('#update-train-confort-class').val());
                    data.averageSpeed = parseInt( $('#update-train-average-speed').val());
                    data.loginId=sessionStorage.getItem("admin_id");
                    // alert(JSON.stringify(data));
                    $http({
                        method:"post",
                        url: "/adminbasic/modifyTrain",
                        withCredentials: true,
                        data:data
                    }).success(function(data, status, headers, config){
                        if (data) {
                            alert("Update train successfully!");
                        }else{
                            alert("Update train failed!");
                        }
                        $window.location.reload();
                    })
                } else {
                    alert("The economyClass, confortClass and averageSpeed must be an integer!");
                }

            },
            onCancel: function () {

            }
        });
    };

    $scope.addTrain = function() {
        $('#add-train-id').val("");
        $('#add-train-economy-class').val("");
        $('#add-train-confort-class').val("");
        $('#add-train-average-speed').val("");

        $('#add-train-table').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                if(parseInt( $('#add-train-economy-class').val()) && parseInt( $('#add-train-confort-class').val()) && parseInt( $('#add-train-average-speed').val())){
                    var data = new Object();
                    data.id = $('#add-train-id').val();
                    data.economyClass = parseInt( $('#add-train-economy-class').val());
                    data.confortClass = parseInt( $('#add-train-confort-class').val());
                    data.averageSpeed = parseInt( $('#add-train-average-speed').val());
                    data.loginId=sessionStorage.getItem("admin_id");
                    // alert(JSON.stringify(data));
                    $http({
                        method:"post",
                        url: "/adminbasic/addTrain",
                        withCredentials: true,
                        data:data
                    }).success(function(data, status, headers, config){
                        if (data) {
                            alert("Add Train successfully!");
                        }else{
                            alert("Add Train failed!");
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