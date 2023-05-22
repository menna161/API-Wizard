from __future__ import absolute_import, print_function
from future.utils import iteritems
import genpy
import rospy
import pymongo
from pymongo import GEO2D
import json
from bson import json_util
from bson.objectid import ObjectId
from datetime import *
from tf2_msgs.msg import TFMessage
import mongodb_store_msgs.srv as dc_srv
import mongodb_store.util as dc_util
from mongodb_store_msgs.msg import StringPair, StringPairList, Insert


def insert_ros_srv(self, req):
    '\n        Receives a\n        '
    obj = dc_util.deserialise_message(req.message)
    meta = dc_util.string_pair_list_to_dictionary(req.meta)
    collection = self._mongo_client[req.database][req.collection]
    if hasattr(obj, 'pose'):
        collection.create_index([('loc', pymongo.GEO2D)])
    if hasattr(obj, 'geotype'):
        collection.create_index([('geoloc', pymongo.GEOSPHERE)])
    stamp = rospy.get_rostime()
    meta['inserted_at'] = datetime.utcfromtimestamp(stamp.to_sec())
    meta['inserted_by'] = req._connection_header['callerid']
    if (hasattr(obj, 'header') and hasattr(obj.header, 'stamp') and isinstance(obj.header.stamp, genpy.Time)):
        stamp = obj.header.stamp
    elif isinstance(obj, TFMessage):
        if obj.transforms:
            transforms = sorted(obj.transforms, key=(lambda m: m.header.stamp), reverse=True)
            stamp = transforms[0].header.stamp
    meta['published_at'] = datetime.utcfromtimestamp(stamp.to_sec())
    meta['timestamp'] = stamp.to_nsec()
    obj_id = dc_util.store_message(collection, obj, meta)
    if self.replicate_on_write:
        for extra_client in self.extra_clients:
            extra_collection = extra_client[req.database][req.collection]
            dc_util.store_message(extra_collection, obj, meta, obj_id)
    return str(obj_id)
