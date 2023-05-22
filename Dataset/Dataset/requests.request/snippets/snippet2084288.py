from __future__ import absolute_import, unicode_literals
from cloudipsp.configuration import __api_url__, __protocol__, __r_type__
from cloudipsp import exceptions
import os
import requests
import logging
import cloudipsp.helpers as helper
import cloudipsp.utils as utils


def _request(self, url, method, data, headers):
    '\n        :param url: request url\n        :param method: request method, POST default\n        :param data: request data\n        :param headers: request headers\n        :return: api response\n        '
    log.debug(('Request Type: %s' % self.request_type))
    log.debug(('URL: %s' % url))
    log.debug(('Data: %s' % str(data)))
    log.debug(('Headers: %s' % str(headers)))
    response = requests.request(method, url, data=data, headers=headers)
    return self._response(response, response.content.decode('utf-8'))
