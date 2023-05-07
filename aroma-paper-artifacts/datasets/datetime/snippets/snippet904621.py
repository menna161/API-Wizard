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


def to_datetime(rt):
    return (datetime.datetime.utcfromtimestamp(rt.secs) + datetime.timedelta(microseconds=(rt.nsecs / 1000)))
