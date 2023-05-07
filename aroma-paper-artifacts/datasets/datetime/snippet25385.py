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


def read_feather(path):
    ' Wrapper function feather.read_dataframe adds date columns from index'
    out_df = pd.read_feather(path)
    out_df['index'] = pd.to_datetime(out_df['index'])
    out_df = out_df.set_index(['index'])
    return out_df
