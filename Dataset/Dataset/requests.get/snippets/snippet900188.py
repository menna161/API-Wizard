import hashlib
import base64
import random
import requests
import yaml
from sawtooth_signing import create_context
from sawtooth_signing import CryptoFactory
from sawtooth_signing import ParseError
from sawtooth_signing.secp256k1 import Secp256k1PrivateKey
from sawtooth_sdk.protobuf.transaction_pb2 import TransactionHeader
from sawtooth_sdk.protobuf.transaction_pb2 import Transaction
from sawtooth_sdk.protobuf.batch_pb2 import BatchList
from sawtooth_sdk.protobuf.batch_pb2 import BatchHeader
from sawtooth_sdk.protobuf.batch_pb2 import Batch


def _send_to_restapi(self, suffix, data=None, contentType=None):
    'Send a REST command to the Validator via the REST API.'
    if self._baseUrl.startswith('http://'):
        url = '{}/{}'.format(self._baseUrl, suffix)
    else:
        url = 'http://{}/{}'.format(self._baseUrl, suffix)
    headers = {}
    if (contentType is not None):
        headers['Content-Type'] = contentType
    try:
        if (data is not None):
            result = requests.post(url, headers=headers, data=data)
        else:
            result = requests.get(url, headers=headers)
        if (not result.ok):
            raise Exception('Error {}: {}'.format(result.status_code, result.reason))
    except requests.ConnectionError as err:
        raise Exception('Failed to connect to {}: {}'.format(url, str(err)))
    except BaseException as err:
        raise Exception(err)
    return result.text
