var priceModule = angular.module("myApp",[]);

priceModule.factory('loadDataService', function ($http, $q) {

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
                alert("Request the Price list fail!" + data.message);
            }
        });
        return promise;
    };

    return service;
});

priceModule.controller("priceCtrl", function ($scope,$http, loadDataService, $window) {

    //首次加载显示数据
    loadDataService.loadAdminBasic("/adminbasic/getAllPrices").then(function (result) {
        console.log(result);
        $scope.prices = result.priceConfig;
    });

    $scope.deletePrice = function(price) {
        $('#delete-price-confirm').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                $http({
                    method:"post",
                    url: "/adminbasic/deletePrice",
                    withCredentials: true,
                    data:{
                        loginId:sessionStorage.getItem("admin_id"),
                        id:price.id,
                        routeId:price.routeId,
                        trainType:price.trainType,
                        basicPriceRate:price.basicPriceRate,
                        firstClassPriceRate:price.firstClassPriceRate
                    }
                }).success(function(data, status, headers, config){
                    if (data) {
                       alert("Delete price successfully!");
                    }else{
                        alert("Update price failed!");
                    }
                    $window.location.reload();
                })
            },
            // closeOnConfirm: false,
            onCancel: function () {

            }
        });
    };

    $scope.updatePrice = function(price) {
        $('#update-price-route-id').val(price.routeId);
        $('#update-price-train-type').val(price.trainType);
        $('#update-price-basic-price-rate').val(price.basicPriceRate);
        $('#update-price-first-class-price-rate').val(price.firstClassPriceRate);

        $('#update-price-table').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                if(parseFloat($('#update-price-basic-price-rate').val()) && parseFloat($('#update-price-first-class-price-rate').val()) ){
                    var data = new Object();
                    data.id = price.id;
                    data.routeId = $('#update-price-route-id').val();
                    data.trainType = $('#update-price-train-type').val();
                    data.basicPriceRate = parseFloat($('#update-price-basic-price-rate').val());
                    data.firstClassPriceRate = parseFloat($('#update-price-first-class-price-rate').val());
                    data.loginId=sessionStorage.getItem("admin_id");
                    // alert(JSON.stringify(data));
                    $http({
                        method:"post",
                        url: "/adminbasic/modifyPrice",
                        withCredentials: true,
                        data:data
                    }).success(function(data, status, headers, config){
                        if (data) {
                            alert("Update price successfully!");
                        }else{
                            alert("Update price failed!");
                        }
                        $window.location.reload();
                    })
                } else {
                    alert("The basic price rate and the first class price rate must be a number!");
                }


            },
            onCancel: function () {

            }
        });
    };

    $scope.addPrice = function() {
        $('#add-price-route-id').val("");
        $('#add-price-train-type').val("");
        $('#add-price-basic-price-rate').val("");
        $('#add-price-first-class-price-rate').val("");

        $('#add-price-table').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                if(parseFloat($('#add-price-basic-price-rate').val()) && parseFloat($('#add-price-first-class-price-rate').val()) ){
                    var data = new Object();
                    data.routeId = $('#add-price-route-id').val();
                    data.trainType = $('#add-price-train-type').val();
                    data.basicPriceRate = parseFloat($('#add-price-basic-price-rate').val());
                    data.firstClassPriceRate = parseFloat($('#add-price-first-class-price-rate').val());
                    data.loginId=sessionStorage.getItem("admin_id");
                    // alert(JSON.stringify(data));
                    $http({
                        method:"post",
                        url: "/adminbasic/addPrice",
                        withCredentials: true,
                        data:data
                    }).success(function(data, status, headers, config){
                        if (data) {
                            alert("Add Price successfully!");
                        }else{
                            alert("Add Price failed!");
                        }
                        $window.location.reload();
                    })
                }  else {
                    alert("The basic price rate and the first class price rate must be a number!");
                }
            },
            onCancel: function () {

            }
        });
    };



});