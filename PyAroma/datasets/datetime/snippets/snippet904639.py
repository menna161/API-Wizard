from __future__ import print_function
import rospy
import mongodb_store.util as mg_util
import sys
import time
import pymongo
from multiprocessing import Process
import calendar
import datetime
import threading
import multiprocessing
from rosgraph_msgs.msg import Clock
import signal
from optparse import OptionParser
import platform
import queue as Queue
import Queue


def setup(self, database_name, req_topics, start_dt, end_dt):
    ' Read in details of requested playback collections. '
    if (database_name not in self.mongo_client.database_names()):
        raise Exception(('Unknown database %s' % database_name))
    database = self.mongo_client[database_name]
    collection_names = database.collection_names(include_system_collections=False)
    req_topics = set(map(mg_util.topic_name_to_collection_name, req_topics))
    if (len(req_topics) > 0):
        topics = req_topics.intersection(collection_names)
        dropped = req_topics.difference(topics)
        if (len(dropped) > 0):
            print(('WARNING Dropped non-existant requested topics for playback: %s' % dropped))
    else:
        topics = set(collection_names)
    print(('Playing back topics %s' % topics))
    collections = [database[collection_name] for collection_name in topics]
    for collection in collections:
        collection.ensure_index(TIME_KEY)
    if (len(start_dt) == 0):
        start_time = to_ros_time(min(map(min_time, [collection for collection in collections if (collection.count() > 0)])))
    else:
        start_time = to_ros_time(mkdatetime(start_dt))
    if (len(end_dt) == 0):
        end_time = to_ros_time(max(map(max_time, [collection for collection in collections if (collection.count() > 0)])))
    else:
        end_time = to_ros_time(mkdatetime(end_dt))
    self.mongo_client.close()
    self.event = multiprocessing.Event()
    pre_roll = rospy.Duration(2)
    post_roll = rospy.Duration(0)
    self.clock_player = ClockPlayer(self.event, start_time, end_time, pre_roll, post_roll)
    self.players = map((lambda c: TopicPlayer(self.mongodb_host, self.mongodb_port, database_name, c, self.event, (start_time - pre_roll), (end_time + post_roll))), topics)
