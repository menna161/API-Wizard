from typing import Any, Dict, Optional
from altair.utils.data import to_values
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
import altair_transform


@pytest.fixture
def lookup_data() -> Dict[(str, Any)]:
    rand = np.random.RandomState(0)
    df = pd.DataFrame({'y': rand.randint(0, 50, 4), 'd': list('ABCD'), 'e': list('ACDE')})
    return to_values(df)
