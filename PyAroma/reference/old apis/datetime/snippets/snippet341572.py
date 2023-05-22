from __future__ import absolute_import, division, print_function, with_statement
from collections import defaultdict
from datetime import datetime
import functools
import time
import sys
from bson.objectid import ObjectId
from turbo.log import model_log
from turbo.util import escape as _es, import_object


def _valid_record(self, record):
    if (not isinstance(record, dict)):
        raise Exception(('%s record is not dict' % record))
    rset = set(record.keys())
    fset = set(self.field.keys())
    rset.discard('_id')
    fset.discard('_id')
    if (not ((fset ^ rset) <= fset)):
        raise Exception(('record keys is not equal to fields keys %s' % list(((fset ^ rset) - fset))))
    for (k, v) in self.field.items():
        if (k not in record):
            if ((v[0] is datetime) and (not v[1])):
                record[k] = self.datetime()
                continue
            if ((v[0] is time) and (not v[1])):
                record[k] = self.timestamp()
                continue
            record[k] = v[1]
    return record
