from __future__ import absolute_import
import datetime
import json
import mimetypes
from multiprocessing.pool import ThreadPool
import os
import re
import tempfile
import six
from six.moves.urllib.parse import quote
from argo.workflows.client.configuration import Configuration
import argo.workflows.client.models
from argo.workflows.client import rest
from dateutil.parser import parse
from dateutil.parser import parse


def __deserialize(self, data, klass):
    'Deserializes dict, list, str into an object.\n\n        :param data: dict, list or str.\n        :param klass: class literal, or string of class name.\n\n        :return: object.\n        '
    if (data is None):
        return None
    if (type(klass) == str):
        if klass.startswith('list['):
            sub_kls = re.match('list\\[(.*)\\]', klass).group(1)
            return [self.__deserialize(sub_data, sub_kls) for sub_data in data]
        if klass.startswith('dict('):
            sub_kls = re.match('dict\\(([^,]*), (.*)\\)', klass).group(2)
            return {k: self.__deserialize(v, sub_kls) for (k, v) in six.iteritems(data)}
        if (klass in self.NATIVE_TYPES_MAPPING):
            klass = self.NATIVE_TYPES_MAPPING[klass]
        else:
            klass = getattr(argo.workflows.client.models, klass)
    if (klass in self.PRIMITIVE_TYPES):
        return self.__deserialize_primitive(data, klass)
    elif (klass == object):
        return self.__deserialize_object(data)
    elif (klass == datetime.date):
        return self.__deserialize_date(data)
    elif (klass == datetime.datetime):
        return self.__deserialize_datatime(data)
    else:
        return self.__deserialize_model(data, klass)
