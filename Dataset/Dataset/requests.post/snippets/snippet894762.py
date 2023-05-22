import json
from base64 import b64encode
from collections import namedtuple
from os import environ, urandom
import requests
import base58
from cryptoconditions import Ed25519Sha256
from pytest import fixture
from sha3 import sha3_256
from bigchaindb_driver.common.transaction import Transaction, _fulfillment_to_details
from bigchaindb_driver.crypto import generate_keypair
from bigchaindb_driver.crypto import generate_keypair
from bigchaindb_driver.crypto import generate_keypair
from bigchaindb_driver import BigchainDB
from bigchaindb_driver import BigchainDB
from uuid import uuid4
from bigchaindb_driver.common.transaction import Transaction
from uuid import uuid4
from bigchaindb_driver.common.transaction import Transaction


@fixture
def mock_requests_post(monkeypatch):

    class MockResponse():

        def __init__(self, json):
            self._json = json

        def json(self):
            return self._json

    def mockreturn(*args, **kwargs):
        return MockResponse(kwargs.get('json'))
    monkeypatch.setattr('requests.post', mockreturn)
