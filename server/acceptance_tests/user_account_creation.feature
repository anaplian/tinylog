Feature: User Account Creation

Scenario: A new user account is successfully created
	Given that no account with the desired username exists
	And the client has correctly solved the captcha
	When a post request is made to the /users resource
	Then the new user should be listed under the /users resource
	And the new user should be available at their /user/<username> url
