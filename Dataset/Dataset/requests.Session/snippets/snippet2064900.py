from __future__ import print_function
import requests
from rinse import ENVELOPE_XSD
from rinse.util import SCHEMA, cached_property
from rinse.response import RinseResponse


@cached_property
def _session(self):
    'Cached instance of requests.Session.'
    return requests.Session()
