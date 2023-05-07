import logging
from datetime import datetime
from functools import wraps
from sanic import Sanic
from sap import cf_logging
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.sanic_logging.context import SanicContext
from sap.cf_logging.sanic_logging.request_reader import SanicRequestReader
from sap.cf_logging.sanic_logging.response_reader import SanicResponseReader


@wraps(wrapped)
def _wrapper(request):
    correlation_id = cf_logging.FRAMEWORK.request_reader.get_correlation_id(request)
    cf_logging.FRAMEWORK.context.set_correlation_id(correlation_id, request)
    cf_logging.FRAMEWORK.context.set('request_started_at', datetime.utcnow(), request)
    return wrapped(request)
