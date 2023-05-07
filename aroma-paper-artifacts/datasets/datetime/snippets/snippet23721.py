import asyncio
import datetime
import json
import os
import aiohttp
import pytest
from aioresponses import aioresponses
from google import auth as gauth
from google.auth import compute_engine
from google.oauth2 import _client as oauth_client
from google.oauth2 import credentials
from google.oauth2 import service_account
from gordon_gcp import exceptions
from gordon_gcp.clients import auth


@pytest.fixture
def mock_parse_expiry(mocker, monkeypatch):
    mock = mocker.MagicMock(oauth_client)
    mock._parse_expiry.return_value = datetime.datetime(2018, 1, 1, 12, 0, 0)
    monkeypatch.setattr('gordon_gcp.clients.auth._client', mock)
    return mock
