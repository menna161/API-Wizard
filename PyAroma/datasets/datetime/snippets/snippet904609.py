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


def update_ros_srv(self, req):
    '\n        Updates a msg in the store\n        '
    collection = self._mongo_client[req.database][req.collection]
    obj_query = self.to_query_dict(req.message_query, req.meta_query)
    obj_query['_meta.stored_type'] = req.message.type
    rospy.logdebug('update spec document: %s', obj_query)
    obj = dc_util.deserialise_message(req.message)
    meta = dc_util.string_pair_list_to_dictionary(req.meta)
    meta['last_updated_at'] = datetime.utcfromtimestamp(rospy.get_rostime().to_sec())
    meta['last_updated_by'] = req._connection_header['callerid']
    (obj_id, altered) = dc_util.update_message(collection, obj_query, obj, meta, req.upsert)
    if self.replicate_on_write:
        for extra_client in self.extra_clients:
            extra_collection = extra_client[req.database][req.collection]
            dc_util.update_message(extra_collection, obj_query, obj, meta, req.upsert)
    return (str(obj_id), altered)
