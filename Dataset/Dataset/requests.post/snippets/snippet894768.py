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
def sent_persisted_random_transaction(alice_pubkey, alice_privkey, transactions_api_full_url):
    from uuid import uuid4
    from bigchaindb_driver.common.transaction import Transaction
    asset = {'data': {'x': str(uuid4())}}
    tx = Transaction.create(tx_signers=[alice_pubkey], recipients=[([alice_pubkey], 1)], asset=asset)
    tx_signed = tx.sign([alice_privkey])
    response = requests.post(transactions_api_full_url, json=tx_signed.to_dict())
    return response.json()
