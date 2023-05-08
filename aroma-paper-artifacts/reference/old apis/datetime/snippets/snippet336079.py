import copy
import datetime
import logging
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.ext import db
from google.appengine.ext import ndb
import json
import simplejson as json


def _json_encode_datetime(o):
    'Json encode a datetime object.\n\n  Args:\n    o: a datetime object.\n\n  Returns:\n    A dict of json primitives.\n  '
    return {'isostr': o.strftime(_DATETIME_FORMAT)}
