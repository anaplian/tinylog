"""Main application entrypoint for the TinyLog API"""

from flask import Flask
# This doesn't conform to PEP-8 but it is idiomatic for Flask
app = Flask(__name__) #pylint: disable=C0103

@app.route('/')
def hello_world():
    """Return a greeting page when the index is requested"""
    return 'Welcome to TinyLog'
