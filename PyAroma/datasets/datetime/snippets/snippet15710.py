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


@wraps(wrapped)
def _wrapper(response):
    cf_logging.FRAMEWORK.context.set('response_sent_at', datetime.utcnow(), request)
    extra = {REQUEST_KEY: request, RESPONSE_KEY: response}
    logging.getLogger('cf.flask.logger').info('', extra=extra)
    return wrapped(response)
