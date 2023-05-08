import logging
import time
from datetime import datetime, timedelta
from typing import List
import pandas as pd
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from box.models import BoxSettings
from data.models import SeenByDay, SeenByHour, TmuxStatus
from data.queries import get_unique_observable_ids_seen
from data.time_utils import as_day, as_hour, get_most_recent_hour, sleep_until_interval_is_complete


def get_unaggregated_days(dt_from: datetime, dt_until: datetime) -> List[datetime]:
    'Look back in time to see which days (start time) are not yet aggregated, but should be.'
    days_without_integration = []
    box_settings = BoxSettings.objects.first()
    for day in pd.date_range(as_day(dt_from), as_day(dt_until), freq='1D'):
        aggregation = SeenByDay.objects.filter(box_id=box_settings.box_id).filter(day_start=day).first()
        if (aggregation is None):
            if (TmuxStatus.objects.filter(time_stamp__gte=day).filter(time_stamp__lt=(day + timedelta(hours=24))).filter(sensor_status=True).count() > 0):
                days_without_integration.append(day)
    return days_without_integration
