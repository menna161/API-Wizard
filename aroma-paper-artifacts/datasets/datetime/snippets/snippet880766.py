import atexit
import datetime
from dateutil.parser import parse
import json
import mimetypes
from multiprocessing.pool import ThreadPool
import os
import re
import tempfile
from urllib.parse import quote
from polyaxon_sdk.configuration import Configuration
import polyaxon_sdk.models
from polyaxon_sdk import rest
from polyaxon_sdk.exceptions import ApiValueError, ApiException


def sanitize_for_serialization(self, obj):
    'Builds a JSON POST object.\n\n        If obj is None, return None.\n        If obj is str, int, long, float, bool, return directly.\n        If obj is datetime.datetime, datetime.date\n            convert to string in iso8601 format.\n        If obj is list, sanitize each element in the list.\n        If obj is dict, return the dict.\n        If obj is OpenAPI model, return the properties dict.\n\n        :param obj: The data to serialize.\n        :return: The serialized form of data.\n        '
    if (obj is None):
        return None
    elif isinstance(obj, self.PRIMITIVE_TYPES):
        return obj
    elif isinstance(obj, list):
        return [self.sanitize_for_serialization(sub_obj) for sub_obj in obj]
    elif isinstance(obj, tuple):
        return tuple((self.sanitize_for_serialization(sub_obj) for sub_obj in obj))
    elif isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    if isinstance(obj, dict):
        obj_dict = obj
    else:
        obj_dict = obj.to_dict()
    return {key: self.sanitize_for_serialization(val) for (key, val) in obj_dict.items()}
