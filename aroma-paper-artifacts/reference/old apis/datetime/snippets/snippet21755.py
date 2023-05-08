import logging
import time
from datetime import datetime
import pytz
from django.conf import settings


def as_hour(dt: datetime) -> datetime:
    return dt.replace(minute=0, second=0, microsecond=0)
