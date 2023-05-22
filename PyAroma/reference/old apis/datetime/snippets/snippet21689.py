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


def aggregate_day(day_start: datetime) -> SeenByDay:
    'Aggregate daily seen events for the day starting at the passed time.'
    box_settings = BoxSettings.objects.first()
    unique_observable_ids_today = get_unique_observable_ids_seen(box_id=box_settings.box_id, start_time=day_start, end_time=(day_start + timedelta(days=1)))
    unique_observable_ids_preceding_day = get_unique_observable_ids_seen(box_id=box_settings.box_id, start_time=(day_start - timedelta(days=1)), end_time=day_start)
    seen_both_today_and_yesterday = [observable_id for observable_id in unique_observable_ids_today if (observable_id in unique_observable_ids_preceding_day)]
    unique_observable_ids_a_week_earlier = get_unique_observable_ids_seen(box_id=box_settings.box_id, start_time=(day_start - timedelta(days=7)), end_time=(day_start - timedelta(days=6)))
    seen_both_today_and_a_week_earlier = [observable_id for observable_id in unique_observable_ids_today if (observable_id in unique_observable_ids_a_week_earlier)]
    aggregation = SeenByDay(box_id=box_settings.box_id, day_start=day_start)
    existing_aggregation = SeenByDay.objects.filter(box_id=box_settings.box_id).filter(day_start=day_start).first()
    if existing_aggregation:
        aggregation = existing_aggregation
    aggregation.seen = len(unique_observable_ids_today)
    aggregation.seen_also_on_preceding_day = len(seen_both_today_and_yesterday)
    aggregation.seen_also_a_week_earlier = len(seen_both_today_and_a_week_earlier)
    return aggregation
