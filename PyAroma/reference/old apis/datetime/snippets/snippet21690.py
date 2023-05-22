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


def get_unaggregated_hours(dt_from: datetime, dt_until: datetime) -> List[datetime]:
    'Look back in time to see which hours (start time) are not yet aggregated, but should be.'
    hours_without_aggregations = []
    box_settings = BoxSettings.objects.first()
    for hour in pd.date_range(as_hour(dt_from), as_hour(dt_until), freq='1H'):
        aggregation = SeenByHour.objects.filter(box_id=box_settings.box_id).filter(hour_start=hour).first()
        if (aggregation is None):
            if (TmuxStatus.objects.filter(time_stamp__gte=hour).filter(time_stamp__lt=(hour + timedelta(hours=1))).filter(sensor_status=True).count() > 0):
                hours_without_aggregations.append(hour)
    return hours_without_aggregations
