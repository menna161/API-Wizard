from option_utilities import read_feather, write_feather
from spx_data_update import UpdateSP500Data, IbWrapper
from ib_insync import IB, Index, util
import numpy as np
import pandas as pd
from arch import arch_model
import matplotlib.pyplot as plt
import matplotlib.cm as cm


@property
def realized_vol(self):
    'Annualized daily volatility calculated as sum of squared 5 minute returns'
    squared_diff = (np.log((self.bars['close'] / self.bars['close'].shift(1))) ** 2)
    realized_quadratic_variation = squared_diff.groupby(squared_diff.index.date).sum()
    realized_quadratic_variation = realized_quadratic_variation.reindex(pd.to_datetime(realized_quadratic_variation.index))
    daily_vol = np.sqrt((realized_quadratic_variation * 252))
    daily_vol = daily_vol.rename('rv_daily')
    return daily_vol
