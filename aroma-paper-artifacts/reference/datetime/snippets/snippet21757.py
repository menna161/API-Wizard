import logging
import time
from datetime import datetime
import pytz
from django.conf import settings


def get_most_recent_hour() -> datetime:
    return as_hour(aileen_now())
