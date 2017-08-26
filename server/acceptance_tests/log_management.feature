Feature: Log management

Scenario: An authenticated user creates a new log
	Given that the user has valid credentials
	And the user makes a POST request to /login
	When the user tries to create a new log
	Then the log should be available at the returned url
	And the log should be listed at the /logs endpoint

Scenario: An authenticated user creates a new log entry
	Given that the user has valid credentials
	And the user makes a POST request to /login
	And the user tries to create a new log
	When the user tries to create a new log entry
	Then the log entry should be available at the returned url
	And the log should be listed in the parent log object
