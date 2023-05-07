from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import re
import json
import tableschema
from slugify import slugify
from dateutil.parser import parse


def restore_row(self, row, schema):
    'Restore row from BigQuery\n        '
    for (index, field) in enumerate(schema.fields):
        if (field.type == 'datetime'):
            row[index] = parse(row[index])
        if (field.type == 'date'):
            row[index] = parse(row[index]).date()
        if (field.type == 'time'):
            row[index] = parse(row[index]).time()
    return schema.cast_row(row)
