import email
import email.errors
import socket
import ssl
import sys
import requests
from urllib.request import Request, build_opener, HTTPErrorProcessor, HTTPSHandler
from urllib.error import URLError
from urllib.parse import urlencode
from urllib2 import Request, URLError, build_opener, HTTPErrorProcessor, HTTPSHandler
from urllib import urlencode


def _http_request_requests(self, url, headers, data, params):
    kwargs = {'verify': self.verify_cert}
    if (url is not None):
        kwargs['url'] = url
    if (headers is not None):
        kwargs['headers'] = headers
    if (data is not None):
        kwargs['data'] = data
    if (params is not None):
        kwargs['params'] = params
    if (self.timeout is not None):
        kwargs['timeout'] = self.timeout
    try:
        if (data is None):
            r = requests.get(**kwargs)
        else:
            r = requests.post(**kwargs)
    except requests.exceptions.RequestException as e:
        raise PanHttpError(('RequestException: ' + str(e)))
    self.code = r.status_code
    self.reason = r.reason
    x = [('%s: %s' % (k, v)) for (k, v) in r.headers.items()]
    try:
        self.headers = email.message_from_string('\n'.join(x))
    except (TypeError, email.errors.MessageError) as e:
        raise PanHttpError(('email.message_from_string() %s' % e))
    self.encoding = self.headers.get_content_charset('utf8')
    self.content_type = self.headers.get_content_type()
    self.content = r.content
    self.text = r.text
