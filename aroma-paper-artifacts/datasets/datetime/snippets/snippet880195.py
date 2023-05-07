import copy
import logging
import multiprocessing
import sys
import urllib3
import http.client as httplib
from polyaxon_sdk.exceptions import ApiValueError


def __init__(self, host=None, api_key=None, api_key_prefix=None, username=None, password=None, access_token=None, server_index=None, server_variables=None, server_operation_index=None, server_operation_variables=None, ssl_ca_cert=None):
    'Constructor\n        '
    self._base_path = ('http://localhost' if (host is None) else host)
    'Default Base url\n        '
    self.server_index = (0 if ((server_index is None) and (host is None)) else server_index)
    self.server_operation_index = (server_operation_index or {})
    'Default server index\n        '
    self.server_variables = (server_variables or {})
    self.server_operation_variables = (server_operation_variables or {})
    'Default server variables\n        '
    self.temp_folder_path = None
    'Temp file folder for downloading files\n        '
    self.api_key = {}
    if api_key:
        self.api_key = api_key
    'dict to store API key(s)\n        '
    self.api_key_prefix = {}
    if api_key_prefix:
        self.api_key_prefix = api_key_prefix
    'dict to store API prefix (e.g. Bearer)\n        '
    self.refresh_api_key_hook = None
    'function hook to refresh API key if expired\n        '
    self.username = username
    'Username for HTTP basic authentication\n        '
    self.password = password
    'Password for HTTP basic authentication\n        '
    self.access_token = access_token
    'Access token\n        '
    self.logger = {}
    'Logging Settings\n        '
    self.logger['package_logger'] = logging.getLogger('polyaxon_sdk')
    self.logger['urllib3_logger'] = logging.getLogger('urllib3')
    self.logger_format = '%(asctime)s %(levelname)s %(message)s'
    'Log format\n        '
    self.logger_stream_handler = None
    'Log stream handler\n        '
    self.logger_file_handler = None
    'Log file handler\n        '
    self.logger_file = None
    'Debug file location\n        '
    self.debug = False
    'Debug switch\n        '
    self.verify_ssl = True
    'SSL/TLS verification\n           Set this to false to skip verifying SSL certificate when calling API\n           from https server.\n        '
    self.ssl_ca_cert = ssl_ca_cert
    'Set this to customize the certificate file to verify the peer.\n        '
    self.cert_file = None
    'client certificate file\n        '
    self.key_file = None
    'client key file\n        '
    self.assert_hostname = None
    'Set this to True/False to enable/disable SSL hostname verification.\n        '
    self.connection_pool_maxsize = (multiprocessing.cpu_count() * 5)
    "urllib3 connection pool's maximum number of connections saved\n           per pool. urllib3 uses 1 connection as default value, but this is\n           not the best value when you are making a lot of possibly parallel\n           requests to the same host, which is often the case here.\n           cpu_count * 5 is used as default value to increase performance.\n        "
    self.proxy = None
    'Proxy URL\n        '
    self.proxy_headers = None
    'Proxy headers\n        '
    self.safe_chars_for_path_param = ''
    'Safe chars for path_param\n        '
    self.retries = None
    'Adding retries to override urllib3 default value 3\n        '
    self.client_side_validation = True
    self.socket_options = None
    'Options to pass down to the underlying urllib3 socket\n        '
    self.datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'
    'datetime format\n        '
    self.date_format = '%Y-%m-%d'
    'date format\n        '
