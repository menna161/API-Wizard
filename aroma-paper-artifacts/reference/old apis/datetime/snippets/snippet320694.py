import hmac
import time
import base64
import hashlib
import datetime
import requests
import logging
import re
from urllib import parse
from collections import OrderedDict
from amazon_pay.payment_response import PaymentResponse, PaymentErrorResponse


def _querystring(self, params):
    "Generate the querystring to be posted to the MWS endpoint\n\n        Required parameters for every API call.\n\n        AWSAccessKeyId: Your Amazon MWS account is identified by your access key,\n            which Amazon MWS uses to look up your secret key.\n\n        SignatureMethod: The HMAC hash algorithm you are using to calculate your\n            signature. Both HmacSHA256 and HmacSHA1 are supported hash algorithms,\n            but Amazon recommends using HmacSHA256.\n\n        SignatureVersion: Which signature version is being used. This is Amazon\n            MWS-specific information that tells Amazon MWS the algorithm you used\n            to form the string that is the basis of the signature. For Amazon MWS,\n            this value is currently SignatureVersion=2.\n\n        Version: The version of the API section being called.\n\n        Timestamp: Each request must contain the timestamp of the request. The\n            Timestamp attribute must contain the client's machine time in\n            ISO8601 format; requests with a timestamp significantly different\n            (15 minutes) than the receiving machine's clock will be rejected to\n            help prevent replay attacks.\n\n        SellerId: Your seller or merchant identifier.\n        "
    parameters = {'AWSAccessKeyId': self.mws_access_key, 'SignatureMethod': 'HmacSHA256', 'SignatureVersion': '2', 'Version': self._api_version, 'Timestamp': (datetime.datetime.utcnow().replace(microsecond=0).isoformat(sep='T') + 'Z')}
    if ('SellerId' not in params):
        parameters['SellerId'] = self.merchant_id
    parameters.update({k: v for (k, v) in params.items()})
    parse_results = parse.urlparse(self._mws_endpoint)
    string_to_sign = 'POST\n{}\n{}\n{}'.format(parse_results[1], parse_results[2], parse.urlencode(sorted(parameters.items())).replace('+', '%20').replace('*', '%2A').replace('%7E', '~'))
    parameters['Signature'] = self._sign(string_to_sign)
    ordered_parameters = OrderedDict(sorted(parameters.items()))
    ordered_parameters.move_to_end('Signature')
    return parse.urlencode(ordered_parameters).encode(encoding='utf_8')
