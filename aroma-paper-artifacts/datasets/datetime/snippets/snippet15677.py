import logging
from datetime import datetime
from sap import cf_logging
from sap.cf_logging import defaults
from sap.cf_logging.core.constants import REQUEST_KEY, RESPONSE_KEY
from sap.cf_logging.core.framework import Framework
from sap.cf_logging.django_logging.context import DjangoContext
from sap.cf_logging.django_logging.request_reader import DjangoRequestReader
from sap.cf_logging.django_logging.response_reader import DjangoResponseReader


def process_request(self, request):
    '\n        Process the request before routing it.\n\n        :param request: - Django Request object\n        '
    framework = cf_logging.FRAMEWORK
    cid = framework.request_reader.get_correlation_id(request)
    framework.context.set_correlation_id(cid, request)
    framework.context.set('request_started_at', datetime.utcnow(), request)
