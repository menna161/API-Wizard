from datetime import date, datetime
from enum import Enum
import json
import logging
import posixpath
import socket
import struct
import time
from urllib.parse import urlparse, urlunparse
import requests
import urllib3
from isilon_hadoop_tools import IsilonHadoopToolError
import isi_sdk_8_2_2
import isi_sdk_7_2
import isi_sdk_8_0
import isi_sdk_8_0_1
import isi_sdk_8_1_0
import isi_sdk_8_1_1
import isi_sdk_8_2_0
import isi_sdk_8_2_1
import isi_sdk_8_2_2


@accesses_onefs
def flush_auth_cache(self, zone=None):
    'Flush the Security Objects Cache.'
    if (self._revision < ONEFS_RELEASES['8.0.1.0']):
        _zone = (zone or self.default_zone)
        if (_zone and (_zone.lower() != 'system')):
            raise UnsupportedOperation('The auth cache can only be flushed on the System zone before OneFS 8.0.1.')
        response = requests.delete(url=(self.host + '/platform/3/auth/users'), verify=self.verify_ssl, auth=(self.username, self.password), params={'cached': True}, timeout=REQUEST_TIMEOUT)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            raise NonSDKAPIError('The auth cache could not be flushed.') from exc
        else:
            assert bool((response.status_code == requests.codes.no_content))
    else:
        try:
            self._sdk.AuthApi(self._api_client).create_auth_cache_item(auth_cache_item=self._sdk.AuthCacheItem(all='all'), zone=(zone or self.default_zone))
        except ValueError as exc:
            assert (str(exc) == 'Invalid value for `id`, must not be `None`')
