"""Main application entrypoint for the TinyLog API"""

import functools
import logging
import os

import envpy
from flask import Flask, abort, jsonify, request

from tinylog_server import recaptcha
from tinylog_server.db import models as tiny_models

# This doesn't conform to PEP-8 but it is idiomatic for Flask
app = Flask(__name__) #pylint: disable=C0103

CONFIG = envpy.get_config({
    "ENV": envpy.Schema(
        value_type=str,
        default="PROD",
    ),
    "CAPTCHA_CHALLENGE": envpy.Schema(
        value_type=str,
    ),
    "DATABASE_DSN": envpy.Schema(
        value_type=str,
    ),
})

SECRETS = envpy.get_config({
    "CAPTCHA_SECRET": envpy.Schema(
        value_type=str,
    ),
})


def init():
    """Initialise app"""
    # Init logging
    logging_handler = logging.StreamHandler()
    logging_formatter = logging.Formatter(\
        "%(asctime)s - %(levelname)s - %(name)s: %(message)s")
    logging_handler.setFormatter(logging_formatter)
    app.logger.addHandler(logging_handler)
    app.logger.setLevel(logging.INFO)

    # Log current config
    app.logger.info('Config loaded: %s', CONFIG)

    # Configure Flask App
    app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG['DATABASE_DSN']

    # Register app with SQLAlchemy
    tiny_models.DB.init_app(app)
init()


# Decorators

def authorized(view):
    @functools.wraps(view)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')

        # Check auth header is provided
        if auth_header is None:
            return jsonify('Authorization header is required'), 400

        # Check auth header is valid
        auth_parts = auth_header.split(' ')
        if len(auth_parts) != 2:
            return jsonify('Invalid Authorization header'), 400

        auth_type, access_token = auth_parts
        if auth_type != 'tinylog':
            return jsonify('Unsupported auth type'), 400

        # Check session exists
        session = tiny_models.Session.query.filter_by(
            access_token=access_token).first()
        if (
            session is None
            or not session.is_valid
        ):
            return jsonify('Invalid access token'), 403

        return view(session, *args, **kwargs)

    return wrapper


# Views

@app.route('/')
def index():
    """Return API Index"""
    return jsonify({
        'users': make_url(request, 'users'),
    })

@app.route('/captcha_challenge')
def captcha_challenge():
    """Returns the token needed to perform a captcha check"""
    return jsonify(CONFIG['CAPTCHA_CHALLENGE'])

@app.route('/users/', methods=['GET', 'POST'])
def users():
    """View and manage users"""
    if request.method == 'GET':
        all_users = tiny_models.User.query.all()
        return jsonify({
            'users': [user.to_dict(request.url_root) for user in all_users],
        })

    elif request.method == 'POST':
        request_data = request.json or {}
        captcha_token = request_data.get('captcha_token')
        username = request_data.get('username')
        password = request_data.get('password')
        display_name = request_data.get('display_name')

        # Validata captcha token
        if (
                captcha_token is None
                or not recaptcha.valid_captcha_token(
                    SECRETS['CAPTCHA_SECRET'],
                    captcha_token
                )
        ):
            return jsonify('Invalid captcha token'), 400

        # Validate user data
        ## Username is required
        if username is None:
            return jsonify('Username is required'), 400
        ## Username must be unique
        existing_user = tiny_models.User.query.filter_by(
            username=username).first()
        if existing_user is not None:
            return jsonify('Username is not available'), 400
        ## Password is required
        if password is None:
            return jsonify('Password is required'), 400

        # Create user in db
        new_user = tiny_models.User(
            username=username,
            password=password,
            display_name=display_name,
        )
        tiny_models.DB.session.add(new_user)
        tiny_models.DB.session.commit()

        return jsonify('User created successfully'), 201

@app.route('/users/<username>/', methods=['GET'])
def user(username):
    """Return the details of a particular user"""
    selected_user = tiny_models.User.query.filter_by(username=username).first()
    if selected_user is None:
        abort(404, 'User does not exist.')
    return jsonify(selected_user.to_dict(request.url_root))

@app.route('/login/', methods=['POST'])
def login():
    """Try to login using the given credentials"""
    request_data = request.json or {}
    username = request_data.get('username')
    password = request_data.get('password')

    # Validate input
    if username is None:
        return jsonify('Username is not required'), 400
    if password is None:
        return jsonify('Password is not required'), 400

    # Check the username/password combo is correct
    selected_user = tiny_models.User.query.filter_by(username=username).first()
    good_creds = (
        selected_user is not None
        and selected_user.is_correct_password(password)
    )
    if not good_creds:
        return jsonify('Incorrect username/password'), 403

    # Create a new session
    session = tiny_models.Session(selected_user.id)
    tiny_models.DB.session.add(session)
    tiny_models.DB.session.commit()

    return jsonify({
        'success': True,
        'access_token': session.access_token,
    }), 200

@app.route('/logout/', methods=['POST'])
@authorized
def logout(session):
    """Invalidate the given access token"""
    tiny_models.DB.session.delete(session)
    tiny_models.DB.session.commit()
    return jsonify("Logged out successfully")

@app.route('/current-user/', methods=['GET'])
@authorized
def current_user(session):
    """Return the currently logged in user"""
    selected_user = tiny_models.User.query.filter_by(id=session.user_id).first()
    return jsonify(selected_user.to_dict(request.url_root))


# Utilities

def make_url(current_request, path):
    """Generate an absolute URL from the request and relative path"""
    return os.path.join(current_request.url_root, path)
