var myApp = angular.module('myApp', [
  'ngRoute',
  'bridgeControllers',
  'ui.bootstrap',
]);

myApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
  when('/analysis', {
    templateUrl: 'partials/analysis.html',
    controller: 'AnalysisController'
  }).
  when('/about', {
    templateUrl: 'partials/about.html',
    controller: 'AboutController'
  }).
  when('/test', {
    templateUrl: 'partials/test.html',
    controller: 'testCont'
  }).
  otherwise({
    redirectTo: '/analysis'
  });
}]);