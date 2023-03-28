from typing import Any, Callable, Dict, List, Tuple, Union
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest
import altair_transform


@pytest.fixture
def data() -> pd.DataFrame:
    rand = np.random.RandomState(42)
    return pd.DataFrame({'x': rand.randint(0, 100, 12), 'y': rand.randint(0, 100, 12), 'i': range(12), 'c': list('AAABBBCCCDDD')})
