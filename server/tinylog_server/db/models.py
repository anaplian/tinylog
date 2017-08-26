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
        self.id = make_random_id()
        self.username = username
        self.display_name = display_name or username
        self.password_hash = PWD_CONTEXT.hash(password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def url(self, url_root):
        return make_url(url_root, 'users/' + self.username)

    def to_dict(self, url_root):
        return {
            '_link': self.url(url_root),
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


class Log(DB.Model):
    id = DB.Column(DB.String(36), primary_key=True)
    name = DB.Column(DB.String(30))
    description = DB.Column(DB.String(255))
    created_at = DB.Column(DB.DateTime)

    entries = DB.relationship("Entry", backref="log")

    def __init__(self, name, description):
        self.id = make_random_id()
        self.name = name
        self.description = description
        self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return '<Log {}, {}>'.format(self.name, self.id)

    def url(self, url_root):
        return make_url(url_root, 'logs/' + self.id)

    def to_dict(self, url_root):
        return {
            '_link': self.url(url_root),
            'name': self.name,
            'description': self.description,
            'entries': [entry.to_dict(url_root) for entry in self.entries],
        }


class Entry(DB.Model):
    id = DB.Column(DB.String(36), primary_key=True)
    title = DB.Column(DB.String(30))
    description = DB.Column(DB.String(255))
    log_id = DB.Column(DB.String, DB.ForeignKey('log.id'))
    created_at = DB.Column(DB.DateTime)

    user_id = DB.Column(DB.String, DB.ForeignKey('user.id'))
    author = DB.relationship("User")

    def __init__(self, title, description, author_id, log_id):
        self.id = make_random_id()
        self.title = title
        self.description = description
        self.user_id = author_id
        self.log_id = log_id
        self.created_at = datetime.datetime.utcnow()

    def url(self, url_root):
        return make_url(url_root, 'logs/' + self.log.id + '/entries/' + self.id)

    def __repr__(self):
        return '<Entry {}, {}>'.format(self.title, self.id)

    def to_dict(self, url_root):
        return {
            '_link': self.url(url_root),
            'title': self.title,
            'description': self.description,
            'log': self.log.url(url_root),
            'author': self.author.url(url_root),
        }


# Utilities

def make_url(url_root, path):
    return os.path.join(url_root, path)

def make_random_id():
    return str(uuid.uuid4())[:8]
