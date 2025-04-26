var contactsModule = angular.module("myApp",[]);

contactsModule.factory('loadDataService', function ($http, $q) {

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
                alert("Request the order list fail!" + data.message);
            }
        });
        return promise;
    };

    return service;
});

contactsModule.controller("contactCtrl", function ($scope,$http, loadDataService, $window) {

    //首次加载显示数据
    loadDataService.loadAdminBasic("/adminbasic/getAllContacts").then(function (result) {
        $scope.contacts = result.contacts;
    });

    $scope.deleteContact = function(contact) {
        $('#delete-contact-confirm').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                // var msg = '你要删除的链接 ID 为 ' + contact.id;
                // alert(msg);
                $http({
                    method:"post",
                    url: "/adminbasic/deleteContacts",
                    withCredentials: true,
                    data:{
                        loginId:sessionStorage.getItem("admin_id"),
                        contactsId:contact.id
                    }
                }).success(function(data, status, headers, config){
                    if (data.status) {
                       alert("Delete contact successfully!");
                    }else{
                        alert(data.message);
                    }
                    $window.location.reload();
                })
            },
            // closeOnConfirm: false,
            onCancel: function () {

            }
        });
    };

    $scope.updateContact = function(contact) {
        $('#update-contact-name').val(contact.name);
        $('#update-contact-document-type').val(contact.documentType);
        $('#update-contact-document-number').val(contact.documentNumber);
        $('#update-contact-phone-number').val(contact.phoneNumber);

        $('#update-contact-table').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                var data = new Object();
                data.contactsId = contact.id;
                data.name =  $('#update-contact-name').val();
                data.documentType = $('#update-contact-document-type').val();
                data.documentNumber = $('#update-contact-document-number').val();
                data.phoneNumber = $('#update-contact-phone-number').val();
                data.loginId=sessionStorage.getItem("admin_id");
                // alert(JSON.stringify(data));
                $http({
                    method:"post",
                    url: "/adminbasic/modifyContacts",
                    withCredentials: true,
                    data:data
                }).success(function(data, status, headers, config){
                    if (data.status) {
                        alert("Update contact successfully!");
                    }else{
                        alert(data.message);
                    }
                    $window.location.reload();
                })
            },
            onCancel: function () {

            }
        });
    };

    $scope.addContact = function() {
        $('#add-contact-account-id').val("");
        $('#add-contact-name').val("");
        $('#add-contact-document-type').val("");
        $('#add-contact-document-number').val("");
        $('#add-contact-phone-number').val("");
        $('#add-contact-table').modal({
            relatedTarget: this,
            onConfirm: function (options) {
                if(parseInt( $('#add-contact-document-type').val())){
                    var data = new Object();
                    data.accountId = $('#add-contact-account-id').val();
                    data.name =  $('#add-contact-name').val();
                    data.documentType = $('#add-contact-document-type').val();
                    data.documentNumber = $('#add-contact-document-number').val();
                    data.phoneNumber = $('#add-contact-phone-number').val();
                    data.loginId=sessionStorage.getItem("admin_id");
                    // alert(JSON.stringify(data));
                    $http({
                        method:"post",
                        url: "/adminbasic/addContacts",
                        withCredentials: true,
                        data:data
                    }).success(function(data, status, headers, config){
                        if (data.status) {
                            alert("Add contact successfully!");
                        }else{
                            alert(data.message);
                        }
                        $window.location.reload();
                    })
                } else{
                    alert("The documentType must be an integer!");
                }


            },
            onCancel: function () {
                // alert('算求，不弄了');
            }
        });
    };

});