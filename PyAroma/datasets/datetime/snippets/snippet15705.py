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


def before_request(wrapped):
    ' Use as a decorator on Flask before_request handler\n    Handles correlation_id by setting it in the context for log records\n    '

    @wraps(wrapped)
    def _wrapper():
        framework = cf_logging.FRAMEWORK
        cid = framework.request_reader.get_correlation_id(request)
        framework.context.set_correlation_id(cid, request)
        framework.context.set('request_started_at', datetime.utcnow(), request)
        return wrapped()
    return _wrapper
