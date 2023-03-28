import logging
import time
from datetime import datetime
import pytz
from django.conf import settings


def as_day(dt: datetime) -> datetime:
    return as_hour(dt).replace(hour=0)
