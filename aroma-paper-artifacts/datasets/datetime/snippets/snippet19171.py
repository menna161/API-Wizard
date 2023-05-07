import logging
from pip._vendor import requests
from pip._vendor.six.moves import xmlrpc_client
from pip._vendor.six.moves.urllib import parse as urllib_parse


def __init__(self, index_url, session, use_datetime=False):
    xmlrpc_client.Transport.__init__(self, use_datetime)
    index_parts = urllib_parse.urlparse(index_url)
    self._scheme = index_parts.scheme
    self._session = session
