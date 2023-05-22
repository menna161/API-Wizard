import os
import pytest
import requests
from requests_mock import Mocker as RequestMocker, ANY
from nautapy.exceptions import NautaLoginException, NautaPreLoginException
from nautapy.nauta_api import CHECK_PAGE, NautaProtocol


def test_nauta_protocol_creates_valid_session():
    with RequestMocker() as mock:
        mget = mock.get(ANY, status_code=200, text=LANDING_HTML)
        mpost = mock.post(ANY, status_code=200, text=LOGIN_HTML)
        (session, login_action, data) = NautaProtocol.create_session()
        assert (mget.called and mpost.called)
        assert isinstance(session, requests.Session)
        assert (login_action and data and data['CSRFHW'] and data['wlanuserip'])
