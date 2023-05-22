from __future__ import division
import contextlib
import json
import numbers
from jsonschema import _utils, _validators
from jsonschema.compat import Sequence, urljoin, urlsplit, urldefrag, unquote, urlopen, str_types, int_types, iteritems, lru_cache
from jsonschema.exceptions import ErrorTree
from jsonschema.exceptions import RefResolutionError, SchemaError, UnknownType
import requests


def resolve_remote(self, uri):
    "\n        Resolve a remote ``uri``.\n\n        If called directly, does not check the store first, but after\n        retrieving the document at the specified URI it will be saved in\n        the store if :attr:`cache_remote` is True.\n\n        .. note::\n\n            If the requests_ library is present, ``jsonschema`` will use it to\n            request the remote ``uri``, so that the correct encoding is\n            detected and used.\n\n            If it isn't, or if the scheme of the ``uri`` is not ``http`` or\n            ``https``, UTF-8 is assumed.\n\n        Arguments:\n\n            uri (str):\n\n                The URI to resolve\n\n        Returns:\n\n            The retrieved document\n\n        .. _requests: http://pypi.python.org/pypi/requests/\n\n        "
    scheme = urlsplit(uri).scheme
    if (scheme in self.handlers):
        result = self.handlers[scheme](uri)
    elif ((scheme in [u'http', u'https']) and requests and (getattr(requests.Response, 'json', None) is not None)):
        if callable(requests.Response.json):
            result = requests.get(uri).json()
        else:
            result = requests.get(uri).json
    else:
        result = json.loads(urlopen(uri).read().decode('utf-8'))
    if self.cache_remote:
        self.store[uri] = result
    return result
