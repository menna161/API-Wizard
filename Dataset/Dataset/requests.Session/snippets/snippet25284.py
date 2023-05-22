import os
import pytest
import requests
from requests_mock import Mocker as RequestMocker, ANY
from nautapy.exceptions import NautaLoginException, NautaPreLoginException
from nautapy.nauta_api import CHECK_PAGE, NautaProtocol


def test_nauta_protocol_login_ok():
    with RequestMocker() as mock:
        mpost = mock.post(ANY, status_code=200, text=LOGGED_IN_HTML, url='http://secure.etecsa.net:8443/online.do?fooo')
        NautaProtocol.login(requests.Session(), 'http://test.com/some_action', {}, 'pepe@nauta.com.cu', 'somepass')
