import logging
import time
from datetime import datetime
import pytz
from django.conf import settings


def naive_utc_from(dt: datetime) -> datetime:
    'Return a naive datetime, that is localised to UTC if it has a timezone.'
    if ((not hasattr(dt, 'tzinfo')) or (dt.tzinfo is None)):
        return dt
    else:
        return dt.astimezone(pytz.utc).replace(tzinfo=None)
