import logging
import time
from datetime import datetime
import importlib
import numpy as np
import pandas as pd
import pytz
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from box.models import BoxSettings
from box.utils.dir_handling import get_sensor, build_tmp_dir_name
from box.utils.privacy_utils import hash_observable_ids
from data.models import Events, Observables
from data.time_utils import sleep_until_interval_is_complete


def update_database_with_new_and_updated_observables(sensor_events_df: pd.DataFrame):
    '\n    From known observables and latest sensor input, we compute what should go to the database:\n\n    We are interested in the most recent events, which we do not yet know about.\n    There is some set computing involved to single these out.\n\n    Based on this information, we also update the observables table (this includes adding new ones seen\n    for the first time). Every observable gets time_last_seen set to what the sensor reported just now.\n    '
    logger.info(f'Length of sensor df: {len(sensor_events_df)}')
    known_observables_df = Observables.to_df()
    if (len(known_observables_df.index) > 0):
        known_observables_df.time_last_seen = known_observables_df.time_last_seen.dt.tz_convert(settings.TIME_ZONE)
    new_observables_events_df = sensor_events_df[(~ sensor_events_df.observable_id.isin(known_observables_df.index))]
    known_observables_df = known_observables_df.append(new_observables_events_df[['observable_id', 'time_seen']].rename(columns={'time_seen': 'time_last_seen'}).set_index('observable_id'), sort=False)
    old_dt = datetime(1970, 1, 1, 1, 1, 1, tzinfo=pytz.timezone(settings.TIME_ZONE))
    events_plus_observable_data_df = sensor_events_df.set_index('observable_id').join(known_observables_df).replace(np.NaN, old_dt)
    updated_events_df = events_plus_observable_data_df[(events_plus_observable_data_df.time_seen > events_plus_observable_data_df.time_last_seen)].drop(columns=['time_last_seen']).append(new_observables_events_df.set_index('observable_id'))
    sensor = get_sensor()
    if hasattr(sensor, 'adjust_event_value'):

        def adjust_event(event_df):
            observable: Observables = Observables.find_observable_by_id(event_df.name)
            last_event_value = None
            try:
                last_event_df = Events.find_by_observable_id(observable.id).iloc[(- 1)]
                last_event_value = last_event_df['value']
            except:
                pass
            (event_df['value'], event_df['observations']) = sensor.adjust_event_value(event_df['value'], last_event_value, event_df['observations'], last_event_df['observations'], observable)
            return event_df
        updated_events_df = updated_events_df.apply(adjust_event, axis=1)
    observables_with_recent_updates_df = updated_events_df[['time_seen']].rename(columns={'time_seen': 'time_last_seen'})
    with transaction.atomic():
        created = Observables.save_from_df(observables_with_recent_updates_df)
        logger.info(f'Finished saving {len(observables_with_recent_updates_df.index)} observables, {created} were new.')
        box_settings = BoxSettings.objects.first()
        if (box_settings is None):
            raise Exception('No box settings yet. Please create some in the admin panel.')
        created = Events.save_from_df(updated_events_df, box_settings.box_id)
        logger.info(f'Finished saving {len(updated_events_df.index)} updated observable events, {created} were new.')
