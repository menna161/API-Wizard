from typing import Callable
import collections
import inspect
from datetime import datetime, date
from enum import Enum
from bson import ObjectId
from flask_babel import lazy_gettext
from .core import AppKernelException
from .validators import Validator, NotEmpty, Unique, Max, Min, Regexp, Email
from .util import default_json_serializer, OBJ_PREFIX
import simplejson as json
import json


def convert_date_time(string):
    return datetime.strptime(string, '%Y-%m-%dT%H:%M:%S.%f')
