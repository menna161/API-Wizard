import logging
import time
from datetime import datetime
import pytz
from django.conf import settings


def aileen_now() -> datetime:
    'The current time of the bvp platform. UTC time, localized to the aileen timezone.'
    return as_aileen_time(datetime.utcnow())
