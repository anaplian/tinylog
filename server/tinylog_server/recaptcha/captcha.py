"""Logic for validating reCAPTCHA challenge responses"""

RECAPTCHA_VALIDATION_URL = "https://www.google.com/recaptcha/api/siteverify"

import requests


def valid_captcha_token(secret, response):
    validation_response = requests.post(
        RECAPTCHA_VALIDATION_URL,
        data={
            'secret': secret,
            'response': response,
        },
    )
    return validation_response.json().get('success', False)
