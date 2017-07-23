"""Main application entrypoint for the TinyLog API"""

import logging

import envpy
from flask import Flask

# This doesn't conform to PEP-8 but it is idiomatic for Flask
app = Flask(__name__) #pylint: disable=C0103

CONFIG = envpy.get_config({
    "ENV": envpy.Schema(
        value_type=str,
        default="PROD"
    ),
})


@app.route('/')
def hello_world():
    """Return a greeting page when the index is requested"""
    return 'Welcome to TinyLog {env}'.format(
        env=CONFIG['ENV'],
    )


def init():
    # Init logging
    logging_handler = logging.StreamHandler()
    logging_formatter = logging.Formatter(\
        "%(asctime)s - %(levelname)s - %(name)s: %(message)s")
    logging_handler.setFormatter(logging_formatter)
    app.logger.addHandler(logging_handler)
    app.logger.setLevel(logging.INFO)

    # Log current config
    app.logger.info('Config loaded: %s', CONFIG)
init()
