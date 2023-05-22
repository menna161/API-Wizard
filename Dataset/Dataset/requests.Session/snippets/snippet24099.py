import logging
import requests
from .utils import make_enum


def __init__(self, breeze_url, api_key, dry_run=False, connection=requests.Session()):
    'Instantiates the BreezeApi with your Breeze account information.\n\n        Args:\n          breeze_url: Fully qualified domain for your organizations Breeze\n                      service.\n          api_key: Unique Breeze API key. For instructions on finding your\n                   organizations API key, see:\n                   http://breezechms.com/docs#extensions_api\n          dry_run: Enable no-op mode, which disables requests from being made.\n                   When combined with debug, this allows debugging requests\n                   without affecting data in your Breeze account.'
    self.breeze_url = breeze_url
    self.api_key = api_key
    self.dry_run = dry_run
    self.connection = connection
    if (not (self.breeze_url and self.breeze_url.startswith('https://') and self.breeze_url.find('.breezechms.'))):
        raise BreezeError('You must provide your breeze_url as ', 'subdomain.breezechms.com')
    if (not self.api_key):
        raise BreezeError('You must provide an API key.')
