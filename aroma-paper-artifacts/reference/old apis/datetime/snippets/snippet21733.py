import logging
from datetime import datetime
from typing import Dict, List
import pandas as pd
from django.conf import settings
from data.models import Events, SeenByDay, SeenByHour


def get_unique_observable_ids_seen(box_id: str, start_time: datetime, end_time: datetime) -> List[str]:
    return [row['observable_id'] for row in Events.objects.filter(box_id=box_id).filter(time_seen__gte=start_time).filter(time_seen__lte=end_time).values('observable_id').distinct().all()]
