import cgi
import datetime
import urllib
import zlib
from graphy import bar_chart
from graphy.backends import google_chart_api
from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.datastore import datastore_rpc
from google.appengine.ext import db
from mapreduce import context
from mapreduce import hooks
from mapreduce import json_util
from mapreduce import util
import json
import simplejson as json


@staticmethod
def create_new(mapreduce_id=None, gettime=datetime.datetime.now):
    'Create a new MapreduceState.\n\n    Args:\n      mapreduce_id: Mapreduce id as string.\n      gettime: Used for testing.\n    '
    if (not mapreduce_id):
        mapreduce_id = MapreduceState.new_mapreduce_id()
    state = MapreduceState(key_name=mapreduce_id, last_poll_time=gettime())
    state.set_processed_counts([], [])
    return state
