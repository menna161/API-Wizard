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


def process_response(self, request, response, resource, req_succeeded):
    'Post-processing of the response (after routing).\n\n        :param request: - Falcon Request object\n        :param response: - Falcon Response object\n        :param resource: - Falcon Resource object to which the request was routed\n        :param req_succeeded: - True if no exceptions were raised while\n            the framework processed and routed the request\n        '
    cf_logging.FRAMEWORK.context.set('response_sent_at', datetime.utcnow(), request)
    extra = {REQUEST_KEY: request, RESPONSE_KEY: response}
    logging.getLogger(self._logger_name).info('', extra=extra)
