import os
import re
import hashlib
import shutil
from tempfile import NamedTemporaryFile
import requests
from requests.exceptions import ReadTimeout
from .apiclient import BaseApiClient, DEFAULT_AUTH, DEFAULT_TIMEOUT
from .apiclient import DEFAULT_RETRIES, LOG, requests
from . import CONNECT_API_URL
from .datamodel import DotAccessDict
from .query import ConnectApiResponse
from .query import ConnectApiFileResponse
from .query import ConnectApiCsvFileResponse
from .util import snake_to_camel_case
from builtins import str as text
from urllib import quote as url_quote
from urllib.parse import quote as url_quote


def head_fusion_file(self, path):
    'Make a HEAD http requests for a fusion file.\n\n        Args:\n            path: the fusion file path\n\n        Returns:\n            the headers as a dict.\n        '
    self._check_auth()
    route = 'fusion/files'
    params = self._prepare_params({'path': path})
    headers = self._prepare_headers()
    try:
        LOG.debug('Requesting query path_info=%s', route)
        url = (self._url + 'fusion/files')
        response = requests.head(url, params=params, headers=headers, auth=self._auth, proxies=self._proxies, timeout=self._timeout)
        response.raise_for_status()
    except requests.HTTPError as req_http_err:
        msg = 'Exception occurred during path_info: %s. Error was: %s'
        LOG.exception(msg, route, response.content)
        self._raise_http_error(response, req_http_err)
    except ReadTimeout:
        msg = 'Read Timeout occured during path_info: %s.'
        LOG.exception(msg, route)
        raise
    return response.headers
