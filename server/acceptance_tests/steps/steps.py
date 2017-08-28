"""Step definitions for acceptance tests"""

import requests
import os

BASE_URL = 'http://localhost:8000'
TEST_USER_CREATED = False


# User creation

@given(u'that no account with the desired username exists')
def step_impl(context):
    pass # No need to do anything here

@given(u'the client has correctly solved the captcha')
def step_impl(context):
    captcha_challenge = requests.get(BASE_URL + '/captcha-challenge').json()
    assert len(captcha_challenge) > 0

@when(u'a post request is made to the /users resource')
def step_impl(context):
    # Normally, this would be given by the captcha provider on success
    # but when testing a dummy token is used since, by design, the captcha
    # cannot be solved automatically!
    captcha_token = "DUMMY_CAPTCHA_TOKEN"
    response = requests.post(BASE_URL + '/users/', json={
        'captcha_token': captcha_token,
        'username': 'pflorrick',
        'display_name': 'Old Pete',
        'password': 'onthecampaigntrail',
    })
    assert response.ok

@then(u'the new user should be listed under the /users resource')
def step_impl(context):
    response = requests.get(BASE_URL + '/users/')
    assert response.ok
    assert any([
        user['username'] == 'pflorrick'
        for user in response.json().get('users', [])
    ])
@then(u'the new user should be available at their /user/<username> url')
def step_impl(context):
    response = requests.get(BASE_URL + '/users/pflorrick/')
    assert response.ok
    expected_response = {
      "_link": BASE_URL + "/users/pflorrick", 
      "display_name": "Old Pete", 
      "username": "pflorrick"
    }
    actual_response = response.json()
    assert expected_response == actual_response

# Login

@given(u'that the user has valid credentials')
def step_impl(context):
    global TEST_USER_CREATED

    if not TEST_USER_CREATED:
        #Create a user and store the credentials
        response = requests.post(BASE_URL + '/users/', json={
            'captcha_token': '123',
            'username': 'agos',
            'display_name': 'Cary Agos',
            'password': 'startanotherfirm',
        })
        assert response.ok
        TEST_USER_CREATED = True

    context.username = 'agos'
    context.password = 'startanotherfirm'

@step(u'the user makes a POST request to /login')
def step_impl(context):
    response = requests.post(BASE_URL + '/login/', json={
        'username': context.username,
        'password': context.password,
    })
    if response.ok:
        access_token = response.json().get('access_token')
        context.access_token = access_token
    else:
        context.access_token = None

@then(u'an access token should be returned')
def step_impl(context):
    assert context.access_token

@then(u'the access token should be valid')
def step_impl(context):
    response = requests.get(BASE_URL + '/current-user/', headers={
        'Authorization': 'tinylog ' + context.access_token,
    })
    assert response.ok

@given(u'that the user does not have valid credentials')
def step_impl(context):
    context.username = 'baduser'
    context.password = 'badpass'

@then(u'an access token should not be returned')
def step_impl(context):
    assert not context.access_token

@when(u'the user makes a POST request to /logout')
def step_impl(context):
    response = requests.post(BASE_URL + '/logout/', headers={
        'Authorization': 'tinylog ' + context.access_token,
    })
    assert response.ok

@then(u'the access token should not be valid')
def step_impl(context):
    response = requests.get(BASE_URL + '/current-user/', headers={
        'Authorization': 'tinylog ' + context.access_token,
    })
    assert not response.ok


# Log Management

## Log Creation

@step(u'the user tries to create a new log')
def step_impl(context):
    response = requests.post(
        BASE_URL + '/logs/',
        headers={
            'Authorization': 'tinylog ' + context.access_token,
        },
        json={
            'name': 'Project named partner',
            'description': 'My attempts to found my own firm',
        },
    )
    assert response.ok
    context.log_url = response.json().get('_link')

@then(u'the log should be available at the returned url')
def step_impl(context):
    response = requests.get(context.log_url, headers={
        'Authorization': 'tinylog ' + context.access_token,
    })
    assert response.ok

    expected_response = {
        '_link': context.log_url,
        'name': 'Project named partner',
        'description': 'My attempts to found my own firm',
        'entries': [],
    }
    actual_response = response.json()
    assert expected_response == actual_response

@then(u'the log should be listed at the /logs endpoint')
def step_impl(context):
    response = requests.get(BASE_URL + '/logs/', headers={
        'Authorization': 'tinylog ' + context.access_token,
    })

    assert any([
        log['_link'] == context.log_url
        for log in response.json().get('logs')
    ])

## Log Entry Creation

@when(u'the user tries to create a new log entry')
def step_impl(context):
    response = requests.post(
        os.path.join(context.log_url, 'entries/'),
        headers={
            'Authorization': 'tinylog ' + context.access_token,
        },
        json={
            'title': 'Brick Walls',
            'description': 'Check out that old t-shirt factory',
        },
    )
    assert response.ok
    context.entry_url = response.json().get('_link')

@then(u'the log entry should be available at the returned url')
def step_impl(context):
    response = requests.get(context.entry_url, headers={
        'Authorization': 'tinylog ' + context.access_token,
    })
    assert response.ok

    expected_response = {
        '_link': context.entry_url,
        'title': 'Brick Walls',
        'description': 'Check out that old t-shirt factory',
        'log': context.log_url,
        'author': BASE_URL + '/users/agos',
    }
    actual_response = response.json()
    assert expected_response == actual_response

@then(u'the log should be listed in the parent log object')
def step_impl(context):
    response = requests.get(context.log_url, headers={
        'Authorization': 'tinylog ' + context.access_token,
    })

    assert any([
        entry['_link'] == context.entry_url
        for entry in response.json().get('entries')
    ])
