var app = angular.module('helicopters', ['btford.modal', 'ngRoute']);

app.factory('myModal', function (btfModal) {
    return btfModal({
        controller: 'MyModalCtrl',
        controllerAs: 'modal',
        templateUrl: 'modal.html'
    });
});

app.config(function ($routeProvider) {
    $routeProvider
        .when('/dashboard', {
            templateUrl: '../partials/routes.html',
            controller: 'routeCtrl'
        })
        .when('/login', {
            templateUrl: '../partials/login.html',
            controller: 'authCtrl'
        })
        .otherwise({
            redirectTo: '/login'
        });
});

app.controller('MyModalCtrl', function ($scope, myModal, $rootScope, $http, $location) {
    $scope.close = function () {
        myModal.deactivate();
    };
    $scope.isNumber = angular.isNumber;
    $scope.createRoute = function (newRoute) {
        var tmp = newRoute.date;
        tmp.setHours(newRoute.arriveTmp.getHours());
        tmp.setMinutes(newRoute.arriveTmp.getMinutes());
        newRoute.arrival = (new Date(tmp)).toJSON();
        tmp.setHours(newRoute.departTmp.getHours());
        tmp.setMinutes(newRoute.departTmp.getMinutes());
        newRoute.departure = (new Date(tmp)).toJSON();
        //$rootScope.routes.push(newRoute);
        newRoute.helipad_id = 1;
        if (angular.isNumber(newRoute.id)) {
            $http.put('http://54.187.229.176:8000/api/v1/helipads/1/destinations/' + newRoute.id + '/', newRoute)
                .success(function () {
                    $location.reload();
                }
            );
        } else {
            $http.post('http://54.187.229.176:8000/api/v1/helipads/1/destinations/', newRoute).success(function (data) {
                $rootScope.routes.push(data);
            });
        }
        myModal.deactivate();
    }
});