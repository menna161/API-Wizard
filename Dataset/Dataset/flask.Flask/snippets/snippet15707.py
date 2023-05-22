import logging
from datetime import datetime
from functools import wraps
import flask
from flask import request
from sap import cf_logging
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.flask_logging.context import FlaskContext
from sap.cf_logging.flask_logging.request_reader import FlaskRequestReader
from sap.cf_logging.flask_logging.response_reader import FlaskResponseReader


def init(app, level=defaults.DEFAULT_LOGGING_LEVEL, custom_fields=None):
    ' Initializes logging in JSON format.\n\n    Adds before and after request handlers to `app` object to enable request info log.\n    :param app: - Flask application object\n    :param level: - valid log level from standard logging package (optional)\n    '
    if (not isinstance(app, flask.Flask)):
        raise TypeError('application should be instance of Flask')
    _init_framework(level, custom_fields=custom_fields)

    @app.before_request
    @before_request
    def _app_before_request():
        pass

    @app.after_request
    @after_request
    def _app_after_request(response):
        return response
