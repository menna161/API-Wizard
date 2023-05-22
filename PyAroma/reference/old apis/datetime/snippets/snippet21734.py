import logging
from datetime import datetime
from typing import Dict, List
import pandas as pd
from django.conf import settings
from data.models import Events, SeenByDay, SeenByHour


def compute_kpis(box_id='None') -> Dict:
    'Compute KPIs for a box, over all available aggregated data.\n        * running_since: datetime\n        * observables_seen_per_day: float\n        * busyness: { by_hour: {hour_of_day: int, num_observables: int, percentage_margin_to_second: float}\n                      by_day: {weekday: str, num_observables: int, percentage_margin_to_second: float}\n                    }\n        * stasis: { by_hour: float (percentage), by_day: float, by_week: float (percentage)}\n    '
    kpis = dict(running_since=None, observables_seen_per_day=None)
    kpis['busyness'] = dict(by_hour=dict(hour_of_day=None, num_observables=None, percentage_margin_to_second=None), by_day=dict(weekday=None, num_observables=None, percentage_margin_to_second=None))
    kpis['stasis'] = dict(by_hour=None, by_day=None, by_week=None)
    first_hour = SeenByHour.objects.filter(box_id=box_id).order_by('hour_start').first()
    if (first_hour is not None):
        kpis['running_since'] = first_hour.hour_start
    seen_by_hour_df = prepare_df_datetime_index(SeenByHour.pdobjects.filter(box_id=box_id).to_dataframe(fieldnames=['hour_start', 'seen', 'seen_also_in_preceding_hour']), time_column='hour_start')
    seen_by_day_df = prepare_df_datetime_index(SeenByDay.pdobjects.filter(box_id=box_id).to_dataframe(fieldnames=['day_start', 'seen', 'seen_also_on_preceding_day', 'seen_also_a_week_earlier']), time_column='day_start')
    if (len(seen_by_hour_df.index) > 0):
        hour_means = seen_by_hour_df.seen.groupby([seen_by_hour_df.index.hour]).mean()
        if (len(hour_means.index) > 1):
            hour_means.sort_values(ascending=False, inplace=True)
            kpis['busyness']['by_hour']['num_observables_mean'] = round(hour_means.mean(), 2)
            kpis['busyness']['by_hour']['hour_of_day'] = hour_means.index[0]
            kpis['busyness']['by_hour']['num_observables'] = round(hour_means[hour_means.index[0]], 2)
            kpis['busyness']['by_hour']['percentage_margin_to_mean'] = round((((hour_means.loc[hour_means.index[0]] - hour_means.mean()) / hour_means.mean()) * 100), 2)
        kpis['stasis']['by_hour'] = round(((seen_by_hour_df.seen_also_in_preceding_hour.mean() / seen_by_hour_df.seen.mean()) * 100), 2)
    if (len(seen_by_day_df.index) > 0):
        day_means = seen_by_day_df.seen.groupby([seen_by_day_df.index.dayofweek]).mean()
        if (len(day_means.index) > 1):
            kpis['busyness']['by_day']['num_observables_mean'] = round(day_means.mean(), 2)
            day_means.sort_values(ascending=False, inplace=True)
            week_day_names = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday')
            kpis['busyness']['by_day']['weekday'] = week_day_names[day_means.index[0]]
            kpis['busyness']['by_day']['num_observables'] = day_means[day_means.index[0]]
            kpis['busyness']['by_day']['percentage_margin_to_mean'] = round((((day_means.loc[day_means.index[0]] - day_means.mean()) / day_means.mean()) * 100), 2)
        kpis['observables_seen_per_day'] = round(seen_by_day_df.seen.mean(), 2)
        kpis['stasis']['by_day'] = round(((seen_by_day_df.seen_also_on_preceding_day.mean() / seen_by_day_df.seen.mean()) * 100), 2)
        kpis['stasis']['by_week'] = round(((seen_by_day_df.seen_also_a_week_earlier.mean() / seen_by_day_df.seen.mean()) * 100), 2)
    return kpis
