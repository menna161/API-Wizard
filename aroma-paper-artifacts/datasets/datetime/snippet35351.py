import binascii
from six import BytesIO, PY3
from six.moves import copyreg
import _codecs
import datetime
import json
import logging
import pickletools
import re
from struct import unpack
import pickle


def datetime_(data, tz=None):
    result = datetime.datetime(dt_bytes(data)).isoformat()
    if (tz is not None):
        result = Instance('datetime', (), dict(value=result, tz=tz))
    return result
