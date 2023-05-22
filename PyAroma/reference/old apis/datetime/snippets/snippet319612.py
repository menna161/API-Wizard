import io
import json
from typing import Any, Dict, List, Optional, Union
import altair as alt
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
from altair_saver import SeleniumSaver
from altair_viewer import get_bundled_script
from selenium.common.exceptions import NoSuchElementException
from altair_saver import SeleniumSaver


def get_tz_offset(tz: Optional[str]=None) -> pd.Timedelta:
    'Get the timezone offset between Python and Javascript for dates with the given timezone.\n\n    Parameters\n    ----------\n    tz : string (optional)\n        The timezone of the input dates\n\n    Returns\n    -------\n    offset : pd.Timedelta\n        The offset between the Javasript representation and the Python representation\n        of a date with the given timezone.\n    '
    ts = pd.to_datetime('2012-01-01').tz_localize(tz)
    df = pd.DataFrame({'t': [ts]})
    out = apply(df, {'timeUnit': 'year', 'field': 't', 'as': 'year'})
    date_in = df.t[0]
    date_out = pd.to_datetime((1000000.0 * out.t))[0].tz_localize(tz)
    return (date_out - date_in)
