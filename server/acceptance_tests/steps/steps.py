"""Step definitions for acceptance tests"""

import requests

BASE_URL = 'http://localhost:8000'


# User creation

@given(u'that no account with the desired username exists')
def step_impl(context):
    pass # No need to do anything here

@given(u'the client has correctly solved the captcha')
def step_impl(context):
    captcha_challenge = requests.get(BASE_URL + '/captcha_challenge').json()
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
