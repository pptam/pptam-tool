var configModule = angular.module("myApp",[]);

configModule.factory('loadDataService', function ($http, $q) {

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
                alert("Request the configure list fail!" + data.message);
            }
        });
        return promise;
    };

    return service;
});

configModule.controller("configCtrl", function ($scope,$http, loadDataService, $window) {

    //首次加载显示数据
    loadDataService.loadAdminBasic("/adminbasic/getAllConfigs").then(function (result) {
        // console.log(result);
        $scope.configs = result.configs;
    });

    $scope.deleteConfig = function(config) {
        $('#delete-config-confirm').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                $http({
                    method:"post",
                    url: "/adminbasic/deleteConfig",
                    withCredentials: true,
                    data:{
                        loginId:sessionStorage.getItem("admin_id"),
                        name:config.name
                    }
                }).success(function(data, status, headers, config){
                    if (data) {
                       alert("Delete config successfully!");
                    }else{
                        alert("Update config failed!");
                    }
                    $window.location.reload();
                })
            },
            // closeOnConfirm: false,
            onCancel: function () {

            }
        });
    };

    $scope.updateConfig = function(config) {
        $('#update-config-name').val(config.name);
        $('#update-config-value').val(config.value);
        $('#update-config-desc').val(config.description);

        $('#update-config-table').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                var data = new Object();
                data.name = $('#update-config-name').val();
                data.value = $('#update-config-value').val();
                data.description = $('#update-config-desc').val();
                data.loginId=sessionStorage.getItem("admin_id");
                // alert(JSON.stringify(data));
                $http({
                    method:"post",
                    url: "/adminbasic/modifyConfig",
                    withCredentials: true,
                    data:data
                }).success(function(data, status, headers, config){
                    if (data) {
                        alert("Update configure successfully!");
                    }else{
                        alert("Update configure failed!");
                    }
                    $window.location.reload();
                })

            },
            onCancel: function () {

            }
        });
    };

    $scope.addConfig = function() {
        $('#add-config-name').val("");
        $('#add-config-value').val("");
        $('#add-config-desc').val("");

        $('#add-config-table').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                var data = new Object();
                data.name = $('#add-config-name').val();
                data.value = $('#add-config-value').val();
                data.description = $('#add-config-desc').val();
                data.loginId=sessionStorage.getItem("admin_id");
                // alert(JSON.stringify(data));
                $http({
                    method:"post",
                    url: "/adminbasic/addConfig",
                    withCredentials: true,
                    data:data
                }).success(function(data, status, headers, config){
                    if (data) {
                        alert("Add Configure successfully!");
                    }else{
                        alert("Add Configure failed!");
                    }
                    $window.location.reload();
                })

            },
            onCancel: function () {

            }
        });
    };



});