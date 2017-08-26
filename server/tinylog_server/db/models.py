"""Database models for TinyLog"""

import datetime
import os
import uuid

from flask_sqlalchemy import SQLAlchemy
from passlib.context import CryptContext

DB = SQLAlchemy()
PWD_CONTEXT = CryptContext(
    schemes=["argon2", "pbkdf2_sha256", "des_crypt"],
    deprecated="auto",
)
SESSION_LENGTH = datetime.timedelta(hours=3)


class User(DB.Model):
    id = DB.Column(DB.String(36), primary_key=True)
    username = DB.Column(DB.String(30), unique=True)
    display_name = DB.Column(DB.String(30))
    password_hash = DB.Column(DB.String(255))

    def __init__(self, username, password, display_name=None):
        self.id = str(uuid.uuid4())
        self.username = username
        self.display_name = display_name or username
        self.password_hash = PWD_CONTEXT.hash(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def to_dict(self, url_root):
        return {
            '_link': make_url(url_root, 'users/' + self.username),
            'username': self.username,
            'display_name': self.display_name,
        }

    def is_correct_password(self, password):
        return PWD_CONTEXT.verify(password, self.password_hash)


class Session(DB.Model):
    access_token = DB.Column(DB.String(36), primary_key=True)
    user_id = DB.Column(DB.String, DB.ForeignKey('user.id'))
    created_at = DB.Column(DB.DateTime)
    expires_at = DB.Column(DB.DateTime)

    def __init__(self, user_id):
        self.access_token = str(uuid.uuid4())
        self.user_id = user_id
        self.created_at = datetime.datetime.utcnow()
        self.expires_at = datetime.datetime.utcnow() + SESSION_LENGTH

    def __repr__(self):
        return '<Session {}>'.format(self.user_id)

    @property
    def is_valid(self):
        return datetime.datetime.utcnow() < self.expires_at


def make_url(url_root, path):
    return os.path.join(url_root, path)
