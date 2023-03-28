import logging
from datetime import datetime
from typing import Dict, List
import pandas as pd
from django.conf import settings
from data.models import Events, SeenByDay, SeenByHour


def data_for_observable_per_unit_time(observable_id):
    bin_size = 'H'
    observable_df = prepare_df_datetime_index(Events.find_observable_by_id(observable_id))
    observable_id = observable_df.observable.resample(bin_size).count().to_frame()
    observable_power = observable_df.observable_power.resample(bin_size).mean().to_frame().round()
    observable_packets = observable_df.packets_captured.resample(bin_size).sum().to_frame()
    id_power_packets = observable_power.join(observable_id).join(observable_packets).dropna().abs().rename(columns={'observable': 'seen_count'}).reset_index()
    id_power_packets['time'] = id_power_packets['time'].map((lambda x: x.replace(tzinfo=None).timestamp()))
    data = id_power_packets.to_dict('records')
    return data
