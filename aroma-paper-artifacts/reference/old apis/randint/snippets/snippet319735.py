from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
import altair_transform
from altair_transform.transform.aggregate import AGG_REPLACEMENTS


@pytest.fixture
def data() -> pd.DataFrame:
    rand = np.random.RandomState(42)
    return pd.DataFrame({'x': rand.randint(0, 100, 12), 'c': list('AAABBBCCCDDD')})
