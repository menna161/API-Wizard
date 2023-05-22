from copy import deepcopy
from datetime import datetime
from hashlib import sha1, md5
from random import SystemRandom
from time import time
from rauth.compat import parse_qsl, urljoin, urlsplit, is_basestring
from rauth.oauth import HmacSha1Signature
from rauth.utils import absolute_url, CaseInsensitiveDict, OAuth1Auth, OAuth2Auth, ENTITY_METHODS, FORM_URLENCODED, get_sorted_params, OPTIONAL_OAUTH_PARAMS
from requests.sessions import Session


@staticmethod
def sign(url, app_id, app_secret, hash_meth='sha1', **params):
    '\n        A signature method which generates the necessary Ofly parameters.\n\n        :param app_id: The oFlyAppId, i.e. "application ID".\n        :type app_id: str\n        :param app_secret: The oFlyAppSecret, i.e. "shared secret".\n        :type app_secret: str\n        :param hash_meth: The hash method to use for signing, defaults to\n            "sha1".\n        :type hash_meth: str\n        :param \\*\\*params: Additional parameters.\n        :type \\*\\*\\params: dict\n        '
    hash_meth_str = hash_meth
    if (hash_meth == 'sha1'):
        hash_meth = sha1
    elif (hash_meth == 'md5'):
        hash_meth = md5
    else:
        raise TypeError('hash_meth must be one of "sha1", "md5"')
    now = datetime.utcnow()
    milliseconds = (now.microsecond // 1000)
    time_format = '%Y-%m-%dT%H:%M:%S.{0}Z'.format(milliseconds)
    ofly_params = {'oflyAppId': app_id, 'oflyHashMeth': hash_meth_str.upper(), 'oflyTimestamp': now.strftime(time_format)}
    url_path = urlsplit(url).path
    signature_base_string = ((app_secret + url_path) + '?')
    if len(params):
        signature_base_string += (get_sorted_params(params) + '&')
    signature_base_string += get_sorted_params(ofly_params)
    if (not isinstance(signature_base_string, bytes)):
        signature_base_string = signature_base_string.encode('utf-8')
    ofly_params['oflyApiSig'] = hash_meth(signature_base_string).hexdigest()
    all_params = dict((tuple(ofly_params.items()) + tuple(params.items())))
    return get_sorted_params(all_params)
