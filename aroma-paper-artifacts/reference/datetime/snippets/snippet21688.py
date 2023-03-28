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


def aggregate_hour(hour_start: datetime) -> SeenByHour:
    'Aggregate hourly seen events for the hour starting at the passed time.'
    box_settings = BoxSettings.objects.first()
    unique_observable_ids_this_hour = get_unique_observable_ids_seen(box_id=box_settings.box_id, start_time=hour_start, end_time=(hour_start + timedelta(hours=1)))
    unique_observable_ids_preceding_hour = get_unique_observable_ids_seen(box_id=box_settings.box_id, start_time=(hour_start - timedelta(hours=1)), end_time=hour_start)
    seen_in_both = [observable_id for observable_id in unique_observable_ids_this_hour if (observable_id in unique_observable_ids_preceding_hour)]
    aggregation = SeenByHour(box_id=box_settings.box_id, hour_start=hour_start)
    existing_aggregation = SeenByHour.objects.filter(box_id=box_settings.box_id).filter(hour_start=hour_start).first()
    if existing_aggregation:
        aggregation = existing_aggregation
    aggregation.seen = len(unique_observable_ids_this_hour)
    aggregation.seen_also_in_preceding_hour = len(seen_in_both)
    return aggregation
