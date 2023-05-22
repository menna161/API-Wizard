import altair as alt
from altair_transform import extract_data, transform_chart
import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def data():
    rand = np.random.RandomState(42)
    return pd.DataFrame({'x': rand.randint(0, 100, 12), 'y': rand.randint(0, 100, 12), 't': pd.date_range('2012-01-15', freq='M', periods=12), 'i': range(12), 'c': list('AAABBBCCCDDD')})
