import calendar
from time import time
import datetime as dt
from pathlib import Path
import numpy as np
import pandas_datareader.data as web
from dateutil.relativedelta import relativedelta
from XmlConverter import XmlConverter
from urllib.request import urlretrieve
import pandas as pd
import pyfolio as pf
import matplotlib.transforms as bbox
from matplotlib import rcParams
from matplotlib import cm
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FormatStrFormatter
import matplotlib.colors as colors


def __get_zero_4date(self, as_of_date, maturity_date, date_adjust):
    'Interpolate yield curve between points'
    maturities = pd.DatetimeIndex([(as_of_date + x) for x in self.relative_dates])
    if date_adjust:
        try:
            zero_yld_curve = self.zero_yields.loc[[as_of_date]]
        except:
            dt_idx = self.zero_yields.index.get_loc(as_of_date, method='pad')
            tmp_zero_dts = self.zero_yields.index[dt_idx]
            zero_yld_curve = self.zero_yields.loc[[tmp_zero_dts]]
    else:
        zero_yld_curve = self.zero_yields.loc[[as_of_date]]
    zero_yld_series = pd.Series(data=zero_yld_curve.values.squeeze(), index=maturities)
    if (not (maturity_date in maturities)):
        zero_yld_series.loc[pd.to_datetime(maturity_date)] = float('nan')
        zero_yld_series = zero_yld_series.sort_index()
    zero_yld_series = zero_yld_series.interpolate(method='polynomial', order=2)
    return zero_yld_series[maturity_date]
