app.controller("authCtrl", function ($scope, $rootScope, $location) {
    $scope.login = function (event) {
        event.preventDefault();
        $location.path('/dashboard');
    }
});