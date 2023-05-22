import copy
import logging
import requests
import sys
import platform
from future.utils import raise_from
from requests.adapters import HTTPAdapter
from .auth import RFTokenAuth
from .query import JSONQueryResponse, CSVQueryResponse, BaseQueryResponse
from .error import JsonParseError, MissingAuthError, AuthenticationError, HttpError
from . import APP_ID
from past.builtins import basestring


def __init__(self, auth, url, proxies=None, timeout=DEFAULT_TIMEOUT, app_name=None, app_version=None, pkg_name=None, pkg_version=None, accept_gzip=True, platform_id=None, api_version=1, verify=True):
    self._url = url
    self._proxies = proxies
    self._timeout = timeout
    self._accept_gzip = accept_gzip
    self.verify = verify
    id_list = []
    if ((app_name is not None) and (app_version is not None)):
        id_list.append(('%s/%s (%s)' % (app_name, app_version, platform.platform())))
    elif (app_name is not None):
        id_list.append(('%s (%s)' % (app_name, platform.platform())))
    if ((pkg_name is not None) and (pkg_version is not None)):
        id_list.append(('%s/%s' % (pkg_name, pkg_version)))
    elif (pkg_name is not None):
        id_list.append(('%s' % pkg_name))
    if (platform_id is not None):
        id_list.append(('%s (%s)' % (APP_ID, platform_id)))
    else:
        id_list.append(('%s' % APP_ID))
    self._app_id = ' '.join(id_list)
    self._request_session = requests.Session()
    adapter = HTTPAdapter(pool_maxsize=REQUESTS_POOL_MAXSIZE, pool_block=True)
    self._request_session.mount('http://', adapter)
    self._request_session.mount('https://', adapter)
    self._auth = None
    if isinstance(auth, requests.auth.AuthBase):
        self._auth = auth
    elif isinstance(auth, basestring):
        self._auth = RFTokenAuth(auth, api_version)
