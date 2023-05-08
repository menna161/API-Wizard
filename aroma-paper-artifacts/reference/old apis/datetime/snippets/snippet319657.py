from functools import singledispatch
from typing import Any
import altair as alt
import numpy as np
import pandas as pd
from .visitor import visit
from ..vegaexpr import eval_vegajs


@eval_value.register(alt.DateTime)
def eval_datetime(value: alt.DateTime) -> pd.Series:
    raise NotImplementedError('Evaluating alt.DateTime object')
