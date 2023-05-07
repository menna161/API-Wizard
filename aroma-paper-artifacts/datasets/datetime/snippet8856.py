from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import re
import json
import tableschema
from slugify import slugify
from dateutil.parser import parse


def convert_type(self, type):
    'Convert type to BigQuery\n        '
    mapping = {'any': 'STRING', 'array': None, 'boolean': 'BOOLEAN', 'date': 'DATE', 'datetime': 'DATETIME', 'duration': None, 'geojson': None, 'geopoint': None, 'integer': 'INTEGER', 'number': 'FLOAT', 'object': None, 'string': 'STRING', 'time': 'TIME', 'year': 'INTEGER', 'yearmonth': None}
    if (type not in mapping):
        message = ('Type %s is not supported' % type)
        raise tableschema.exceptions.StorageError(message)
    return mapping[type]
