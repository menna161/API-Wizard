import re
from typing import Union, Set
import pandas as pd
from dateutil.tz import tzlocal


def _compute_timeunit(name: str, date: pd.DatetimeIndex) -> pd.DatetimeIndex:
    'Workhorse for compute_timeunit.'
    if (name in ['day', 'utcday']):
        return (pd.to_datetime('2012-01-01') + pd.to_timedelta(((date.dayofweek + 1) % 7), 'D'))
    units = _parse_timeunit_string(name)
    if ('day' in units):
        raise NotImplementedError('quarter and day timeunit')
    if (not units):
        raise ValueError(f'{0!r} is not a recognized timeunit')

    def quarter(month: pd.Int64Index) -> pd.Int64Index:
        return (month - ((month - 1) % 3))
    Y = (date.year.astype(str) if ('year' in units) else '2012')
    M = (date.month.astype(str).str.zfill(2) if ('month' in units) else (quarter(date.month).astype(str).str.zfill(2) if ('quarter' in units) else '01'))
    D = (date.day.astype(str).str.zfill(2) if ('date' in units) else '01')
    h = (date.hour.astype(str).str.zfill(2) if ('hours' in units) else '00')
    m = (date.minute.astype(str).str.zfill(2) if ('minutes' in units) else '00')
    s = (date.second.astype(str).str.zfill(2) if ('seconds' in units) else '00')
    ms = ((date.microsecond // 1000).astype(str).str.zfill(3) if ('milliseconds' in units) else '00')
    return pd.to_datetime(((((((((((((Y + '-') + M) + '-') + D) + ' ') + h) + ':') + m) + ':') + s) + '.') + ms))
