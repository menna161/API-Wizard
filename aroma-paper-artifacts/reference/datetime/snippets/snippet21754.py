import logging
import time
from datetime import datetime
import pytz
from django.conf import settings


def localized_datetime(dt: datetime) -> datetime:
    'Localise a datetime to the timezone of Aileen'
    return get_timezone().localize(naive_utc_from(dt))
