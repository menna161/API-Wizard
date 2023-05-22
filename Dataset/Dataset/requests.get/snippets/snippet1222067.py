import json
import math
import os
import platform
import random
import re
import sys
import time
from collections import OrderedDict
from io import StringIO
import requests
import numpy as np
from scipy import optimize


def queryMaterials(query, mapiKey):
    'Return a list of material IDs for a given query string'
    if (query[0:3] == 'mp-'):
        return [query]
    try:
        r = requests.get(f'{urlBase}/v2/materials/{query}/mids', headers={'X-API-KEY': mapiKey})
        resp = r.json()
    except Exception as e:
        print(str(e), file=sys.stderr)
        return []
    if (not resp['valid_response']):
        return []
    return resp['response']
