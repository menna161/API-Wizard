from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from pandas.testing import assert_series_equal, assert_frame_equal
import pytest
import altair_transform


@pytest.fixture
def data() -> pd.DataFrame:
    rand = np.random.RandomState(1)
    return pd.DataFrame({'x': rand.randint(0, 100, 12), 'c': list('AAABBBCCCDDD')})
