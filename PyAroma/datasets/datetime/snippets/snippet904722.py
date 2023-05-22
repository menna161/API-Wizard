from __future__ import print_function, absolute_import
import rospy
import genpy
from std_srvs.srv import Empty
import yaml
from bson import json_util, Binary
import json
import copy
import platform
from mongodb_store_msgs.msg import SerialisedMessage
from mongodb_store_msgs.srv import MongoQueryMsgRequest
from pymongo.errors import ConnectionFailure
import importlib
from datetime import datetime
import io as StringIO
import StringIO
import pymongo
import pymongo
import functools
from pymongo import Connection
from pymongo import MongoClient


def add_soma_fields(msg, doc):
    '\n    For soma Object msgs adds the required fields as indexes to the mongodb object.\n    '
    if hasattr(msg, 'pose'):
        doc['loc'] = [doc['pose']['position']['x'], doc['pose']['position']['y']]
    if hasattr(msg, 'logtimestamp'):
        doc['timestamp'] = datetime.utcfromtimestamp(doc['logtimestamp'])
    if hasattr(msg, 'geotype'):
        if (doc['geotype'] == 'Point'):
            for p in doc['geoposearray']['poses']:
                doc['geoloc'] = {'type': doc['geotype'], 'coordinates': [p['position']['x'], p['position']['y']]}
        if (msg._type == 'soma_msgs/SOMAROIObject'):
            coordinates = []
            doc['geotype'] = 'Polygon'
            for p in doc['geoposearray']['poses']:
                coordinates.append([p['position']['x'], p['position']['y']])
            coordinates2 = []
            coordinates2.append(coordinates)
            doc['geoloc'] = {'type': doc['geotype'], 'coordinates': coordinates2}
