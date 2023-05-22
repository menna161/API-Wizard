from __future__ import absolute_import
import rospy
import actionlib
import pymongo
import os
import re
import shutil
import subprocess
from bson import json_util
import sys
import time
from threading import Thread, Lock
from mongodb_store_msgs.msg import MoveEntriesAction, MoveEntriesFeedback
from datetime import datetime
import mongodb_store.util
from mongodb_store_msgs.msg import MoveEntriesAction, MoveEntriesFeedback
from Queue import Queue
from queue import Queue


def do_delete(self, collection, master, less_time_time=None, db='message_store', query=None):
    coll = master[db][collection]
    spec = dict()
    if (query is not None):
        spec.update(query)
    if (less_time_time is not None):
        spec.update({'_meta.inserted_at': {'$lt': datetime.utcfromtimestamp(less_time_time.to_sec())}})
    coll.remove(spec)
