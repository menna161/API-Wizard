from dateutil.tz import tzlocal
import pytest
import pandas as pd
from altair_transform.utils import timeunit


@pytest.mark.parametrize('timezone', TIMEZONES)
@pytest.mark.parametrize('unit', TIMEUNITS)
def test_timeunit_input_types(dates, timezone, unit):
    dates = dates.tz_localize(timezone)
    timestamps = [timeunit.compute_timeunit(d, unit) for d in dates]
    series = timeunit.compute_timeunit(pd.Series(dates), unit)
    datetimeindex = timeunit.compute_timeunit(dates, unit)
    assert isinstance(timestamps[0], pd.Timestamp)
    assert isinstance(series, pd.Series)
    assert isinstance(datetimeindex, pd.DatetimeIndex)
    assert datetimeindex.equals(pd.DatetimeIndex(series))
    assert datetimeindex.equals(pd.DatetimeIndex(timestamps))
