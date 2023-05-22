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


def perf_stats(returns: pd.Series, **kwargs):
    ' Wrapper function for pf.timeseries.performance'
    performance = pf.timeseries.perf_stats(returns, **kwargs)
    perf_index = list(performance.index)
    (performance['StartDate'], performance['EndDate']) = list(returns.index[[0, (- 1)]].strftime('%b %d, %Y'))
    performance = performance.reindex((['StartDate', 'EndDate'] + perf_index))
    performance = performance.rename(returns.name)
    performance = performance.drop('common_sense_ratio', axis=0)
    return performance
