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


def __deserialize(self, data, klass):
    'Deserializes dict, list, str into an object.\n\n        :param data: dict, list or str.\n        :param klass: class literal, or string of class name.\n\n        :return: object.\n        '
    if (data is None):
        return None
    if (type(klass) == str):
        if klass.startswith('List['):
            sub_kls = re.match('List\\[(.*)]', klass).group(1)
            return [self.__deserialize(sub_data, sub_kls) for sub_data in data]
        if klass.startswith('Dict['):
            sub_kls = re.match('Dict\\[([^,]*), (.*)]', klass).group(2)
            return {k: self.__deserialize(v, sub_kls) for (k, v) in data.items()}
        if (klass in self.NATIVE_TYPES_MAPPING):
            klass = self.NATIVE_TYPES_MAPPING[klass]
        else:
            klass = getattr(polyaxon_sdk.models, klass)
    if (klass in self.PRIMITIVE_TYPES):
        return self.__deserialize_primitive(data, klass)
    elif (klass == object):
        return self.__deserialize_object(data)
    elif (klass == datetime.date):
        return self.__deserialize_date(data)
    elif (klass == datetime.datetime):
        return self.__deserialize_datetime(data)
    else:
        return self.__deserialize_model(data, klass)
