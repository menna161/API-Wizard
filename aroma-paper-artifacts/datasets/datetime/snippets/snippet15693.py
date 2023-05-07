import logging
from datetime import datetime
import falcon
from sap import cf_logging
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.falcon_logging.context import FalconContext
from sap.cf_logging.falcon_logging.request_reader import FalconRequestReader
from sap.cf_logging.falcon_logging.response_reader import FalconResponseReader


def process_request(self, request, response):
    'Process the request before routing it.\n\n        :param request: - Falcon Request object\n        :param response: - Falcon Response object\n        '
    framework = cf_logging.FRAMEWORK
    cid = framework.request_reader.get_correlation_id(request)
    framework.context.set_correlation_id(cid, request)
    framework.context.set('request_started_at', datetime.utcnow(), request)
