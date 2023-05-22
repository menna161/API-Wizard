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
def text_search_assets(api_root, transactions_api_full_url, alice_pubkey, alice_privkey):
    response = requests.get((api_root + '/assets'), params={'search': 'bigchaindb'})
    response = response.json()
    if (len(response) == 3):
        assets = {}
        for asset in response:
            assets[asset['id']] = asset['data']
        return assets
    assets = [{'msg': 'Hello BigchainDB 1!'}, {'msg': 'Hello BigchainDB 2!'}, {'msg': 'Hello BigchainDB 3!'}]
    assets_by_txid = {}
    for asset in assets:
        tx = Transaction.create(tx_signers=[alice_pubkey], recipients=[([alice_pubkey], 1)], asset=asset, metadata={"But here's my number": 'So call me maybe'})
        tx_signed = tx.sign([alice_privkey])
        requests.post(transactions_api_full_url, json=tx_signed.to_dict())
        assets_by_txid[tx_signed.id] = asset
    return assets_by_txid
