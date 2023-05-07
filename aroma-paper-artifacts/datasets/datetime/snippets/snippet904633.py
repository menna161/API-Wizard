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


def queue_from_db(self, running):
    self.collection.ensure_index(TIME_KEY)
    documents = self.collection.find({TIME_KEY: {'$gte': to_datetime(self.start_time), '$lte': to_datetime(self.end_time)}}, sort=[(TIME_KEY, pymongo.ASCENDING)])
    if (documents.count() == 0):
        rospy.logwarn(('No messages to play back from topic %s' % self.collection_name))
        return
    else:
        rospy.logdebug('Playing back %d messages', documents.count())
    msg_cls = mg_util.load_class(documents[0]['_meta']['stored_class'])
    latch = False
    if ('latch' in documents[0]['_meta']):
        latch = documents[0]['_meta']['latch']
    self.publisher = rospy.Publisher(documents[0]['_meta']['topic'], msg_cls, latch=latch, queue_size=10)
    for document in documents:
        if running.value:
            message = mg_util.dictionary_to_message(document, msg_cls)
            self.to_publish.put((message, to_ros_time(document['_meta']['inserted_at'])))
        else:
            break
    rospy.logdebug(('All messages queued for topic %s' % self.collection_name))
