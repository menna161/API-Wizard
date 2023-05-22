import logging
import random
import sys
import uuid
from datetime import datetime, timedelta
from typing import Optional
import iso8601
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from data.models import SeenByDay, SeenByHour
from data.time_utils import get_most_recent_hour, get_timezone
from server.models import AileenBox


def makeup_number_observables(dt: datetime, options: dict) -> float:
    weekday_multipliers = [1, 1.1, 1.45, 1.31, 1, 1, 1.13]
    x = (options['base_busyness'] * random.gauss(1, 0.05))
    if ((dt.hour >= 23) or (dt.hour <= 8)):
        x *= (2 / 3)
    if ((options['peak_time'] == 'morning') and (10 <= dt.hour <= 13)):
        x *= 1.5
        if (dt.hour == 11):
            x *= 1.17
    if ((options['peak_time'] == 'afternoon') and (16 <= dt.hour <= 19)):
        x *= 1.5
        if (dt.hour == 17):
            x *= 1.15
    x *= weekday_multipliers[dt.weekday()]
    return x
