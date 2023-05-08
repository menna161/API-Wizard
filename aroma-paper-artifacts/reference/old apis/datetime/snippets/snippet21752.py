import logging
import time
from datetime import datetime
import pytz
from django.conf import settings


def as_aileen_time(dt: datetime) -> datetime:
    'The datetime represented in the timezone of the bvp platform.'
    return naive_utc_from(dt).replace(tzinfo=pytz.utc).astimezone(get_timezone())
