import logging
from datetime import datetime
from sap import cf_logging
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.django_logging.context import DjangoContext
from sap.cf_logging.django_logging.request_reader import DjangoRequestReader
from sap.cf_logging.django_logging.response_reader import DjangoResponseReader


def process_response(self, request, response):
    '\n        Post-processing of the response (after routing).\n\n        :param request: - Django Request object\n        :param request: - Django Response object\n        '
    cf_logging.FRAMEWORK.context.set('response_sent_at', datetime.utcnow(), request)
    extra = {REQUEST_KEY: request, RESPONSE_KEY: response}
    logging.getLogger(self._logger_name).info('', extra=extra)
    return response
