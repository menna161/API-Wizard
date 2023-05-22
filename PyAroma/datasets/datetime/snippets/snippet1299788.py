import datetime
import functools
from io import BytesIO
import ssl
import time
import weakref
from tornado.concurrent import Future, future_set_result_unless_cancelled, future_set_exception_unless_cancelled
from tornado.escape import utf8, native_str
from tornado import gen, httputil
from tornado.ioloop import IOLoop
from tornado.util import Configurable
from typing import Type, Any, Union, Dict, Callable, Optional, cast, Awaitable
from tornado.options import define, options, parse_command_line
from tornado.simple_httpclient import SimpleAsyncHTTPClient


def __init__(self, url: str, method: str='GET', headers: Union[(Dict[(str, str)], httputil.HTTPHeaders)]=None, body: Union[(bytes, str)]=None, auth_username: str=None, auth_password: str=None, auth_mode: str=None, connect_timeout: float=None, request_timeout: float=None, if_modified_since: Union[(float, datetime.datetime)]=None, follow_redirects: bool=None, max_redirects: int=None, user_agent: str=None, use_gzip: bool=None, network_interface: str=None, streaming_callback: Callable[([bytes], None)]=None, header_callback: Callable[([str], None)]=None, prepare_curl_callback: Callable[([Any], None)]=None, proxy_host: str=None, proxy_port: int=None, proxy_username: str=None, proxy_password: str=None, proxy_auth_mode: str=None, allow_nonstandard_methods: bool=None, validate_cert: bool=None, ca_certs: str=None, allow_ipv6: bool=None, client_key: str=None, client_cert: str=None, body_producer: Callable[([Callable[([bytes], None)]], 'Future[None]')]=None, expect_100_continue: bool=False, decompress_response: bool=None, ssl_options: Union[(Dict[(str, Any)], ssl.SSLContext)]=None) -> None:
    'All parameters except ``url`` are optional.\n\n        :arg str url: URL to fetch\n        :arg str method: HTTP method, e.g. "GET" or "POST"\n        :arg headers: Additional HTTP headers to pass on the request\n        :type headers: `~tornado.httputil.HTTPHeaders` or `dict`\n        :arg body: HTTP request body as a string (byte or unicode; if unicode\n           the utf-8 encoding will be used)\n        :arg body_producer: Callable used for lazy/asynchronous request bodies.\n           It is called with one argument, a ``write`` function, and should\n           return a `.Future`.  It should call the write function with new\n           data as it becomes available.  The write function returns a\n           `.Future` which can be used for flow control.\n           Only one of ``body`` and ``body_producer`` may\n           be specified.  ``body_producer`` is not supported on\n           ``curl_httpclient``.  When using ``body_producer`` it is recommended\n           to pass a ``Content-Length`` in the headers as otherwise chunked\n           encoding will be used, and many servers do not support chunked\n           encoding on requests.  New in Tornado 4.0\n        :arg str auth_username: Username for HTTP authentication\n        :arg str auth_password: Password for HTTP authentication\n        :arg str auth_mode: Authentication mode; default is "basic".\n           Allowed values are implementation-defined; ``curl_httpclient``\n           supports "basic" and "digest"; ``simple_httpclient`` only supports\n           "basic"\n        :arg float connect_timeout: Timeout for initial connection in seconds,\n           default 20 seconds\n        :arg float request_timeout: Timeout for entire request in seconds,\n           default 20 seconds\n        :arg if_modified_since: Timestamp for ``If-Modified-Since`` header\n        :type if_modified_since: `datetime` or `float`\n        :arg bool follow_redirects: Should redirects be followed automatically\n           or return the 3xx response? Default True.\n        :arg int max_redirects: Limit for ``follow_redirects``, default 5.\n        :arg str user_agent: String to send as ``User-Agent`` header\n        :arg bool decompress_response: Request a compressed response from\n           the server and decompress it after downloading.  Default is True.\n           New in Tornado 4.0.\n        :arg bool use_gzip: Deprecated alias for ``decompress_response``\n           since Tornado 4.0.\n        :arg str network_interface: Network interface or source IP to use for request.\n           See ``curl_httpclient`` note below.\n        :arg collections.abc.Callable streaming_callback: If set, ``streaming_callback`` will\n           be run with each chunk of data as it is received, and\n           ``HTTPResponse.body`` and ``HTTPResponse.buffer`` will be empty in\n           the final response.\n        :arg collections.abc.Callable header_callback: If set, ``header_callback`` will\n           be run with each header line as it is received (including the\n           first line, e.g. ``HTTP/1.0 200 OK\\r\\n``, and a final line\n           containing only ``\\r\\n``.  All lines include the trailing newline\n           characters).  ``HTTPResponse.headers`` will be empty in the final\n           response.  This is most useful in conjunction with\n           ``streaming_callback``, because it\'s the only way to get access to\n           header data while the request is in progress.\n        :arg collections.abc.Callable prepare_curl_callback: If set, will be called with\n           a ``pycurl.Curl`` object to allow the application to make additional\n           ``setopt`` calls.\n        :arg str proxy_host: HTTP proxy hostname.  To use proxies,\n           ``proxy_host`` and ``proxy_port`` must be set; ``proxy_username``,\n           ``proxy_pass`` and ``proxy_auth_mode`` are optional.  Proxies are\n           currently only supported with ``curl_httpclient``.\n        :arg int proxy_port: HTTP proxy port\n        :arg str proxy_username: HTTP proxy username\n        :arg str proxy_password: HTTP proxy password\n        :arg str proxy_auth_mode: HTTP proxy Authentication mode;\n           default is "basic". supports "basic" and "digest"\n        :arg bool allow_nonstandard_methods: Allow unknown values for ``method``\n           argument? Default is False.\n        :arg bool validate_cert: For HTTPS requests, validate the server\'s\n           certificate? Default is True.\n        :arg str ca_certs: filename of CA certificates in PEM format,\n           or None to use defaults.  See note below when used with\n           ``curl_httpclient``.\n        :arg str client_key: Filename for client SSL key, if any.  See\n           note below when used with ``curl_httpclient``.\n        :arg str client_cert: Filename for client SSL certificate, if any.\n           See note below when used with ``curl_httpclient``.\n        :arg ssl.SSLContext ssl_options: `ssl.SSLContext` object for use in\n           ``simple_httpclient`` (unsupported by ``curl_httpclient``).\n           Overrides ``validate_cert``, ``ca_certs``, ``client_key``,\n           and ``client_cert``.\n        :arg bool allow_ipv6: Use IPv6 when available?  Default is True.\n        :arg bool expect_100_continue: If true, send the\n           ``Expect: 100-continue`` header and wait for a continue response\n           before sending the request body.  Only supported with\n           ``simple_httpclient``.\n\n        .. note::\n\n            When using ``curl_httpclient`` certain options may be\n            inherited by subsequent fetches because ``pycurl`` does\n            not allow them to be cleanly reset.  This applies to the\n            ``ca_certs``, ``client_key``, ``client_cert``, and\n            ``network_interface`` arguments.  If you use these\n            options, you should pass them on every request (you don\'t\n            have to always use the same values, but it\'s not possible\n            to mix requests that specify these options with ones that\n            use the defaults).\n\n        .. versionadded:: 3.1\n           The ``auth_mode`` argument.\n\n        .. versionadded:: 4.0\n           The ``body_producer`` and ``expect_100_continue`` arguments.\n\n        .. versionadded:: 4.2\n           The ``ssl_options`` argument.\n\n        .. versionadded:: 4.5\n           The ``proxy_auth_mode`` argument.\n        '
    self.headers = headers
    if if_modified_since:
        self.headers['If-Modified-Since'] = httputil.format_timestamp(if_modified_since)
    self.proxy_host = proxy_host
    self.proxy_port = proxy_port
    self.proxy_username = proxy_username
    self.proxy_password = proxy_password
    self.proxy_auth_mode = proxy_auth_mode
    self.url = url
    self.method = method
    self.body = body
    self.body_producer = body_producer
    self.auth_username = auth_username
    self.auth_password = auth_password
    self.auth_mode = auth_mode
    self.connect_timeout = connect_timeout
    self.request_timeout = request_timeout
    self.follow_redirects = follow_redirects
    self.max_redirects = max_redirects
    self.user_agent = user_agent
    if (decompress_response is not None):
        self.decompress_response = decompress_response
    else:
        self.decompress_response = use_gzip
    self.network_interface = network_interface
    self.streaming_callback = streaming_callback
    self.header_callback = header_callback
    self.prepare_curl_callback = prepare_curl_callback
    self.allow_nonstandard_methods = allow_nonstandard_methods
    self.validate_cert = validate_cert
    self.ca_certs = ca_certs
    self.allow_ipv6 = allow_ipv6
    self.client_key = client_key
    self.client_cert = client_cert
    self.ssl_options = ssl_options
    self.expect_100_continue = expect_100_continue
    self.start_time = time.time()
