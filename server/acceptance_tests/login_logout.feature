Feature: Login/logout

Scenario: A user logs in with the correct username/password
	Given that the user has valid credentials
	When the user makes a POST request to /login
	Then an access token should be returned
	And the access token should be valid

Scenario: A user logs in with an incorrect username/password
	Given that the user does not have valid credentials
	When the user makes a POST request to /login
	Then an access token should not be returned

Scenario: A currently logged in user logs out
	Given that the user has valid credentials
	And the user makes a POST request to /login
	When the user makes a POST request to /logout
	Then the access token should not be valid
