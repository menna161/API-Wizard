from datetime import datetime, timedelta
import time


def __getattr__(self, item):
    return getattr(self._datetime, item)
