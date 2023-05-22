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


def queryElasticityV2(mat, mapiKey):
    'Return elastic properties for a given material ID, using V2 MAPI'
    data = {'criteria': (('{"task_id": "' + mat) + '"}'), 'properties': '["formula", "pretty_formula", "material_id", "elasticity"]', 'API_KEY': mapiKey}
    try:
        r = requests.post(f'{urlBase}/v2/query', data)
        resp = r.json()
    except Exception as e:
        print(str(e), file=sys.stderr)
        return None
    if (not resp['valid_response']):
        return None
    if (len(resp['response']) > 1):
        raise Exception('Multiple results returned')
    if (len(resp['response']) == 0):
        return None
    return resp['response'][0]
