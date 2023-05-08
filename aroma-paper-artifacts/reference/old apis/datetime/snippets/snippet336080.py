import copy
import datetime
import logging
from google.appengine.api import datastore_errors
from google.appengine.api import datastore_types
from google.appengine.ext import db
from google.appengine.ext import ndb
import json
import simplejson as json


def _json_decode_datetime(d):
    'Converts a dict of json primitives to a datetime object.'
    return datetime.datetime.strptime(d['isostr'], _DATETIME_FORMAT)
