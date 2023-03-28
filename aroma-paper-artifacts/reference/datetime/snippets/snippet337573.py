import base64
import datetime
import itertools
import os
import tarfile
from bson import ObjectId
from flask import make_response, jsonify
from appkernel.core import MessageType
from babel.messages.extract import extract_python
import ast
from appkernel import Model


def default_json_serializer(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    elif isinstance(obj, datetime.timedelta):
        return (datetime.datetime.min + obj).time().isoformat()
    elif isinstance(obj, str):
        return obj.decode('utf-8')
    elif isinstance(obj, ObjectId):
        return '{}{}'.format(OBJ_PREFIX, str(obj))
    else:
        str(obj)
