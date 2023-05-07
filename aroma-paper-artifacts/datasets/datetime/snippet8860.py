from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import re
import json
import tableschema
from slugify import slugify
from dateutil.parser import parse


def restore_type(self, type):
    'Restore type from BigQuery\n        '
    mapping = {'BOOLEAN': 'boolean', 'DATE': 'date', 'DATETIME': 'datetime', 'INTEGER': 'integer', 'FLOAT': 'number', 'STRING': 'string', 'TIME': 'time'}
    if (type not in mapping):
        message = ('Type %s is not supported' % type)
        raise tableschema.exceptions.StorageError(message)
    return mapping[type]
