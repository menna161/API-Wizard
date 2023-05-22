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


def __init__(self, host, port, db, collection, dump_path, less_time=None, query=None):
    cmd = ['mongodump', '--verbose', '-o', dump_path, '--host', host, '--port', str(port), '--db', db, '--collection', collection]
    if (query is None):
        query = {}
    if (less_time is not None):
        query.update({'_meta.inserted_at': {'$lt': datetime.utcfromtimestamp(less_time.to_sec())}})
    if query:
        query = json_util.dumps(query)
        cmd += ['--query', query]
    super(MongoDumpProcess, self).__init__(cmd=cmd)
