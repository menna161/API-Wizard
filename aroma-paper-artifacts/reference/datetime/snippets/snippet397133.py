from __future__ import absolute_import
from __future__ import print_function
from __future__ import division
from builtins import str
from builtins import map
from builtins import object
import datetime
import glob
import os
import re
import time
from qtpy import QtCore
from qtpy import QtGui
from qtpy import QtWidgets
import opencue
from opencue.compiled_proto import job_pb2
import cuegui.AbstractTreeWidget
import cuegui.AbstractWidgetItem
import cuegui.Constants
import cuegui.eta
import cuegui.Logger
import cuegui.MenuActions
import cuegui.Style
import cuegui.ThreadPool
import cuegui.Utils


@staticmethod
def getTimeString(timestamp):
    'Gets a timestamp formatted as a string.'
    tstring = None
    if (timestamp and (timestamp > 0)):
        tstring = datetime.datetime.fromtimestamp(timestamp).strftime('%m/%d %H:%M')
    return tstring
