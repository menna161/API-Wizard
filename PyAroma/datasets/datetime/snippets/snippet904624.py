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


def main(argv):
    myargv = rospy.myargv(argv=argv)
    parser = OptionParser()
    parser.usage += ' [TOPICs...]'
    parser.add_option('--mongodb-name', dest='mongodb_name', help='Name of DB from which to retrieve values', metavar='NAME', default='roslog')
    parser.add_option('-s', '--start', dest='start', type='string', default='', metavar='S', help='start datetime of query, defaults to the earliest date stored in db, across all requested collections. Formatted "d/m/y H:M" e.g. "06/07/14 06:38"')
    parser.add_option('-e', '--end', dest='end', type='string', default='', metavar='E', help='end datetime of query, defaults to the latest date stored in db, across all requested collections. Formatted "d/m/y H:M" e.g. "06/07/14 06:38"')
    (options, args) = parser.parse_args(myargv)
    database_name = options.mongodb_name
    topics = set(args[1:])
    playback = MongoPlayback()

    def signal_handler(signal, frame):
        playback.stop()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    playback.setup(database_name, topics, options.start, options.end)
    playback.start()
    playback.join()
    rospy.set_param('use_sim_time', False)
