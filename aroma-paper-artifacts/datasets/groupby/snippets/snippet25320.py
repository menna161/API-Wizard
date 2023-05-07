from option_utilities import read_feather, write_feather
from spx_data_update import UpdateSP500Data, IbWrapper
from ib_insync import IB, Index, util
import numpy as np
import pandas as pd
from arch import arch_model
import matplotlib.pyplot as plt
import matplotlib.cm as cm


@property
def daily_return(self):
    daily_ret = self.bars['close'].groupby(self.bars.index.date).last().pct_change()
    return daily_ret
