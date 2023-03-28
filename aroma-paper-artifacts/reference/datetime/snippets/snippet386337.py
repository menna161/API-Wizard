import datetime
import time


def __init__(self, offset=None, name=None):
    if (offset is not None):
        self._offset = datetime.timedelta(minutes=offset)
    if (name is not None):
        self._name = name
