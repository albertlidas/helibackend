app.controller("routeCtrl", function ($scope, myModal, $rootScope, $http) {
    $http.get('http://54.187.229.176:8000/api/v1/helipads/1/destinations/').success(function (data) {
        console.log(data);
        $rootScope.routes = data;
    });
    $scope.editMode = false;
    //$rootScope.routes = [
    //    {
    //        location:"Odessa",
    //        to:"Minsk",
    //        departure: new Date("2016-02-28T14:36:59.448Z"),
    //        arrival: new Date("2016-02-28T14:36:59.448Z"),
    //        pilot1:"Vasya",
    //        pilot2:"Petya",
    //        board:"747",
    //        info:"bla-bla",
    //        place1: true,
    //        place2: false,
    //        place3: false,
    //        place4: true
    //    },
    //    {
    //        location:"Odessa",
    //        to:"Minsk",
    //        departure:new Date("2016-02-28T14:36:59.448Z"),
    //        arrival:new Date("2016-02-28T14:36:59.448Z"),
    //        pilot1:"Vasya",
    //        pilot2:"Petya",
    //        board:"747",
    //        info:"bla-bla",
    //        place1: false,
    //        place2: true,
    //        place3: false,
    //        place4: true
    //    },
    //    {
    //        location:"Odessa",
    //        to:"Minsk",
    //        departure:new Date("2016-02-28T14:36:59.448Z"),
    //        arrival:new Date("2016-02-28T14:36:59.448Z"),
    //        pilot1:"Vasya",
    //        pilot2:"Petya",
    //        board:"747",
    //        info:"bla-bla",
    //        place1: false,
    //        place2: true,
    //        place3: true,
    //        place4: false
    //    }
    //];

    $scope.selectRoute = function (route) {
        if ($scope.editMode) {
            $rootScope.newRoute = route;
            $rootScope.newRoute.arriveTmp = new Date($rootScope.newRoute.arrival);
            $rootScope.newRoute.departTmp = new Date($rootScope.newRoute.departure);
            $rootScope.newRoute.date = new Date($rootScope.newRoute.arrival);
            myModal.activate();
        } else {
            $scope.currentRoute = route;
        }
    };

    $scope.selectPlace = function (place, num) {
        $scope.currentPlace = {
            value: place,
            number: num
        };
    };
    $scope.addRoute = function () {
        myModal.activate();
        $rootScope.newRoute = {};
    };

    $scope.removeRoute = function (id, index) {
        $http.delete('http://54.187.229.176:8000/api/v1/helipads/1/destinations/' + id + '/').success(function () {
            $rootScope.routes.splice(index, 1);
        })
    };
    $scope.switchMode = function () {
        $scope.editMode = !$scope.editMode;
    }
});