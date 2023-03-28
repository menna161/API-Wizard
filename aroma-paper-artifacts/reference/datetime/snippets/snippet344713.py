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


def __deserialize_datatime(self, string):
    'Deserializes string to datetime.\n\n        The string should be in iso8601 datetime format.\n\n        :param string: str.\n        :return: datetime.\n        '
    try:
        from dateutil.parser import parse
        return parse(string)
    except ImportError:
        return string
    except ValueError:
        raise rest.ApiException(status=0, reason='Failed to parse `{0}` as datetime object'.format(string))
