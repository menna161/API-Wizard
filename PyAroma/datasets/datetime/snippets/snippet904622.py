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


def ros_time_strftime(rt, format):
    ' converts a ros time to a datetime and calls strftime on it with the given format '
    return to_datetime(rt).strftime(format)
