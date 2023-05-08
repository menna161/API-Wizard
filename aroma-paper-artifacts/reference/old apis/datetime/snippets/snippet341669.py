import inspect
import os
import sys
from datetime import datetime, date
import time
import json
from collections import Iterable
import copy
import base64
from bson.objectid import ObjectId
from turbo.log import util_log
from base64 import decodebytes, encodebytes
from base64 import encodestring as encodebytes, decodestring as decodebytes
from turbo.model import BaseModel


def format_time(dt):
    'datetime format\n    '
    return time.mktime(dt.timetuple())
