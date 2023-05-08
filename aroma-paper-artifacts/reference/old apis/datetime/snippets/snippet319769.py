import altair as alt
import pandas as pd
from pandas.testing import assert_frame_equal


def test_tz_code(driver):
    code = driver.get_tz_code()
    pd.to_datetime('2012-01-01').tz_localize(code)
