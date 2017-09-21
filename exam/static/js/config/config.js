'use strict';


app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});


app.config(function($provide) {
  $provide.decorator('$log', function($delegate, $sniffer) {
        var _log = $delegate.log; //Saving the original behavior

        $delegate.log = function(message) { };
        $delegate.error = function(message) {
            // alert(message);
            // Code here for
        }

        return $delegate;
    });
})
