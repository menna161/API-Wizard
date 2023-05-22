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


def matlab2datetime(matlab_datenum):

    def matlab_convert_2_datetime(single_date):
        day = dt.datetime.fromordinal(int(single_date))
        dayfrac = (dt.timedelta(days=(single_date % 1)) - dt.timedelta(days=366))
        return (day + dayfrac)
    try:
        python_dates = [matlab_convert_2_datetime(int(dts)) for dts in matlab_datenum]
    except TypeError:
        print(matlab_datenum, 'is not iterable')
    return pd.DatetimeIndex(python_dates)
