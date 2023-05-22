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
def persisted_carol_bicycle_transaction(transactions_api_full_url, signed_carol_bicycle_transaction):
    response = requests.post(transactions_api_full_url, json=signed_carol_bicycle_transaction)
    return response.json()
