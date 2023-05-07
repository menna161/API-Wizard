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


def __init__(self, update_data=True):
    self.relative_dates = ([relativedelta(days=1), relativedelta(months=3), relativedelta(months=6)] + [relativedelta(years=x) for x in range(1, 31)])
    fed_zero_feather = Path((self.DB_PATH / 'fedzero.feather'))
    if update_data:
        if fed_zero_feather.is_file():
            seconds_since_update = (time() - fed_zero_feather.stat().st_mtime)
            zero_yields_old = read_feather(str(fed_zero_feather))
            latest_business_date = (pd.to_datetime('today') - pd.tseries.offsets.BDay(1))
            if (zero_yields_old.index[(- 1)].date() != latest_business_date.date()):
                if (seconds_since_update > (3600 * 12)):
                    self.get_raw_zeros()
        else:
            self.get_raw_zeros()
    self.zero_yields = read_feather(str(fed_zero_feather))
