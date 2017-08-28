import angular from 'angular';
import 'angular-cookies';
require('angular-route');

import '../style/app.css';

const app = angular.module('app', ['ngRoute', 'ngCookies']);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider){
	  $routeProvider.when('/', {
        template: '<root></root>'
    }).otherwise({
        template: '404 - not the droids you\'re looking for'
    });
}]);

app.run(['$rootScope', 'auth', '$location', function($rootScope, auth, $location){
  //$rootScope.$on('$routeChangeStart', function(event, next, current){
    //$location.url('/');
		/*desiredPath = '/';
    routeIsRestricted = false;
    try {
      desiredPath = next.$$route.originalPath;
      routeIsRestricted = next.$$route.data.restricted;
    } catch(e){
      console.log("Could not redirect:" + e);
    }
        
    if(desiredPath === '/' && auth.isLoggedIn) {
      $location.url('/log');
    }
    
    if(routeIsRestricted && !auth.isLoggedIn){
      $location.url('/login');
    } */
  //})
}]);


app.controller('rootController', function () {
	    this.message = "hello worlb";
});
app.controller('navigationController', function () {
	    this.message = "hello worlb";
});
app.controller('logController', function () {
	    this.message = "hello worlb";
});
app.controller('searchController', function () {
	    this.message = "hello worlb";
});
app.controller('entryController', function () {
	    this.message = "hello worlb";
});

app.directive('root', function(){
  return {
    scope: {},
    controller: 'rootController',
    controllerAs: 'ctrl',
    template: require('./views/root.html')
  }
});

app.directive('navigation', function(){
	return {
		scope: {},
		controller: 'navigationController',
		controllerAs: 'ctrl',
		template: require('./views/navigation.html')
	}
});

app.directive('log', function(){
	return {
		scope: {},
		controller: 'logController',
		controllerAs: 'ctrl',
		template: require('./views/log.html')
	}
});

app.directive('entry', function(){
	return {
		scope: {},
		controller: 'entryController',
		controllerAs: 'ctrl',
		template: require('./views/entry.html')
	}
});

app.directive('search', function(){
	return {
		scope: {},
		controller: 'searchController',
		controllerAs: 'ctrl',
		template: require('./views/search.html')
	}
});

/** SERVICES */

app.service('database', ["$http", function($http){
	var database = this;

	database.checkSessionIsValid = function() {

	};

	database.login = function(username, password) {

	};

	database.signup = function(username, email, password) {

	};
}]);

app.service('auth', ['$http', 'database', '$cookies', '$location', function auth($http, database, $cookies, $location){
		var auth = this;

		auth.isLoggedIn = false;
		auth.sessionToken = "";
		auth.userID = -1;
		auth.username = "";
	

		auth.checkSession = function(){
			return database.checkSessionIsValid().then(
				function(response){
					if(!response.status===200){
						auth.isLoggedIn = false;
					}

				}
			);
		};

		if(!!$cookies.get('sessionToken')){
			//sessionToken is defined
			if(!auth.userID || auth.userID ==-1){

				auth.isLoggedIn = $cookies.get('isLoggedIn');
				auth.sessionToken = $cookies.get('sessionToken');
				auth.userID = $cookies.get('userID');
				auth.username = $cookies.get('username');

				auth.checkSession();
			}	
		}

	
		auth.login = function(username, password){
			return database.login(username, password).then(
				//success
				function(response){
					auth.userID = response.data.user.id;
					auth.sessionToken = response.data.user.token;
					auth.isLoggedIn = response.data.authorized;
					auth.username = username;

					//set cookie
					$cookies.put('sessionToken', auth.sessionToken);
					$cookies.put('username', auth.username);
					$cookies.put('isLoggedIn', auth.isLoggedIn);
					$cookies.put('userID', auth.userID);

					return;
				},

				//failure
				function(response){
					auth.userID = -1;
					auth.sessionToken = "";
					auth.isLoggedIn = false;
					auth.username = "";

					return response;
				}
			)
		};

		auth.logout = function(){
			return $http({
				method:"DELETE",
				url:"api/sessions"
			}).then(
				function(){
					auth.sessionToken = "";
					auth.isLoggedIn = false;
					auth.username = "";

					//delete cookie
					$cookies.remove('sessionToken');
					$cookies.remove('username');
					$cookies.remove('isLoggedIn');
					$cookies.remove('userID');
					$location.url('/out');
			})};

		auth.signup = function(username, email, password){
			
			return database.signup(username, email, password);

		};

}]);