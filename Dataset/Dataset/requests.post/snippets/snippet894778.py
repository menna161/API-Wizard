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
def persisted_transfer_carol_car_to_dimi(carol_keypair, dimi_pubkey, transactions_api_full_url, persisted_carol_car_transaction):
    output_txid = persisted_carol_car_transaction['id']
    ed25519_dimi = Ed25519Sha256(public_key=base58.b58decode(dimi_pubkey))
    transaction = {'asset': {'id': output_txid}, 'metadata': None, 'operation': 'TRANSFER', 'outputs': ({'amount': '1', 'condition': {'details': _fulfillment_to_details(ed25519_dimi), 'uri': ed25519_dimi.condition_uri}, 'public_keys': (dimi_pubkey,)},), 'inputs': ({'fulfillment': None, 'fulfills': {'output_index': 0, 'transaction_id': output_txid}, 'owners_before': (carol_keypair.public_key,)},), 'version': '2.0', 'id': None}
    serialized_transaction = json.dumps(transaction, sort_keys=True, separators=(',', ':'), ensure_ascii=False)
    serialized_transaction = sha3_256(serialized_transaction.encode())
    if transaction['inputs'][0]['fulfills']:
        serialized_transaction.update('{}{}'.format(transaction['inputs'][0]['fulfills']['transaction_id'], transaction['inputs'][0]['fulfills']['output_index']).encode())
    ed25519_carol = Ed25519Sha256(public_key=base58.b58decode(carol_keypair.public_key))
    ed25519_carol.sign(serialized_transaction.digest(), base58.b58decode(carol_keypair.private_key))
    transaction['inputs'][0]['fulfillment'] = ed25519_carol.serialize_uri()
    set_transaction_id(transaction)
    response = requests.post(transactions_api_full_url, json=transaction)
    return response.json()
