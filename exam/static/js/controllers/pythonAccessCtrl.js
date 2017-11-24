'use strict';

 this.getAccessPython = function(parameter){
        return Restangular.all("get_something_from_angular_to_python").post(parameter, {}, {'Current-Url': window.location.hash});
    }

function pythonAccessCtrl($scope, $http, pythonAccessAPI, SweetAlert, ngNotify, toaster , $uibModal, $timeout, ngTableParams, $filter) {

    var vm = this;
//
//    pythonAccessAPI.getAccessPython({ "param": 3 }).then(function(response) {
//        var temp = response.plain().data;
//        console.log(temp);
//    });

    getAccessPython({ "param": 3 }).then(function(response) {
        var temp = response.plain().data;
        console.log(temp);
    });


    // vm.statusInits = [{"id":"A", "name":"Active"},{"id":"I", "name":"Inactive"}];
    // vm.data = {}

    /*
    vm.clickUpdateApplication = function(appViewForm) {
    vm.isLoading = true;
    if(vm.isSelectedVote == null) {
        vm.isLoading = false;
      swal({
        title: "Please Selected Application",
        text: "",
        timer: 1000,
        showConfirmButton: false
      });
    }else{
      var valueClick = vm.isSelectedVote[0][0];
      applicationAPI.viewApp({ "valueView": valueClick }).then(function(response) {
        if(response.plain().response_code == '20000'){
          vm.isLoading = false;
          var modalInstance = $uibModal.open({
            templateUrl : '/static/views/applicationUpdate.html',
            size : 'lg',
            backdrop: 'static',
            controller : modalFunction,
            controllerAs : 'ctrl',
            resolve:{
              vm: vm,
              appViewForm: appViewForm
            }
          });

          function modalFunction(vm, appViewForm, applicationAPI, $uibModal, $uibModalInstance) {
            var vmModal = this;
            vmModal.appId = response.plain().response_desc.idp_app_id;
            vmModal.appNo = response.plain().response_desc.application_no;
            vmModal.appName = response.plain().response_desc.application_name;
            vmModal.appSingleSignOnURL = response.plain().response_desc.singleSignOnURL;
            vmModal.appAduienceRestriction = response.plain().response_desc.audienceRestriction;
            vmModal.appMetadata = response.plain().response_desc.metadata
            vmModal.appSignOnMethod = response.plain().response_desc.signOnMethod
            vmModal.appLocation = response.plain().response_desc.location;
            vmModal.appENV = response.plain().response_desc.env;
            vmModal.id = response.plain().response_desc.application_id;

            // vmModal.tempStatus = response.plain().response_desc
            // console.log(vmModal.tempStatus)
            vmModal.statusInits = vm.statusInits;
            vmModal.tempStatus = vmModal.statusInits.find(obj => { return obj.id == response.plain().response_desc.status ? obj : null; })

            var old = {
              "appName": vmModal.appName,
              "appAduienceRestriction": vmModal.appAduienceRestriction,
              "appLocation": vmModal.appLocation,
              "appENV": vmModal.appENV,
              "appStatus": vmModal.tempStatus.id,
              "appSingleSignOnURL": vmModal.appSingleSignOnURL
            }

            vmModal.cancelUpdateApplication = function(){
              $uibModalInstance.close();
            }

            vmModal.updateApplication = function(form){
              var firstError = null;
              if(form.$invalid) {
                var field = null, firstError = null;
                for (field in form) {
                  if (field[0] != '$') {
                      if (firstError === null && !form[field].$valid) {
                          firstError = form[field].$name;
                      }

                      if (form[field].$pristine) {
                          form[field].$dirty = true;
                      }
                  }
                }

                angular.element('.ng-invalid[name=' + firstError + ']').focus();
                return;
              }else{
                swal({
                  title: "Are you sure?",
                  text: "",
                  type: "warning",
                  showCancelButton: true,
                  confirmButtonColor: "#DD6B55",
                  confirmButtonText: "Yes, update it!",
                  cancelButtonText: "No, cancel",
                  closeOnConfirm: true,
                  closeOnCancel: false
                },
                function(isConfirm){
                  if (isConfirm) {
                    vmModal.viewLoading = true;
                    var parameter = {
                      "applicationId": vmModal.appId,
                      "applicationNo": vmModal.appNo,
                      "applicationName": vmModal.appName,
                      "appStatus": vmModal.tempStatus.id,
                      "url": vmModal.appSingleSignOnURL,
                      "audienceRestriotion": vmModal.appAduienceRestriction,
                      "appLocation": vmModal.appLocation,
                      "appENV": vmModal.appENV,
                      "id": vmModal.id,
                      "appType": vmModal.appSignOnMethod
                    }

                    var appAttributes = {
                      "sso_url": parameter.url,
                      "audience_url": parameter.audienceRestriotion
                    }

                    var data = {
                      "code": parameter.applicationNo,
                      "name": parameter.applicationName,
                      "type": parameter.appType,
                      "status": parameter.appStatus,
                      "attributes": appAttributes,
                      "location": parameter.appLocation,
                      "env": parameter.appENV,
                      "id": parameter.id
                    };

                    var parameter = {
                      "data": data
                    }

                    applicationAPI.updateSMALApp(parameter).then(function(response_update) {
                      if(response_update.plain().meta.response_code == '20000'){

                        var parameter = {
                          "application_no": vm.data.application_no,
                          "application_name": vm.data.application_name,
                          "application_type": vm.data.application_type ? vm.data.application_type.id : "",
                          "application_status": vm.data.application_status ? vm.data.application_status.id : ""
                        };

                        genTable(parameter);

                        vmModal.viewLoading = true;

                        swal({
                          title: "Successfully Edit",
                          text: "",
                          timer: 1000,
                          showConfirmButton: false
                        });

                        $uibModalInstance.close();
                      }else{
                        vmModal.viewLoading = false;
                        swal(response_update.plain().meta.response_desc)
                        $uibModalInstance.close();
                      }
                    });
                  } else {
                    swal("Cancelled", "", "error");
                  }
                });
              }
            } // end updateApplication
          } // end modalFunction
        }else{
          vm.isLoading = false;
          swal(response.plain().response_desc)
        }
      }); // end applicationAPI.viewApp
    }
  }
  */
}

pythonAccessCtrl.$inject = ['$scope', '$http', 'pythonAccessAPI', 'SweetAlert', 'ngNotify', 'toaster', '$uibModal', '$timeout', 'ngTableParams', '$filter'];
app.controller('pythonAccessCtrl', pythonAccessCtrl);
