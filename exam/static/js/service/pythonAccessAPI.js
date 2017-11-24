'use strict';

app.service('pythonAccessAPI', function(Restangular) {

    this.getAccessPython = function(parameter){
        return Restangular.all("get_something_from_angular_to_python").post(parameter, {}, {'Current-Url': window.location.hash});
    }
});
