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


def get_raw_zeros(self):
    'Update zero coupon yields from FED and FRED'
    try:
        print('Updating zero coupon yields')
        start_time = time()
        urlretrieve(self.ZERO_URL, (self.DB_PATH / 'feds200628.xls'))
        converter = XmlConverter(input_path=(str(self.DB_PATH) + '/feds200628.xls'), first_header='SVENY01', last_header='TAU2')
        converter.parse()
        gsw_zero = converter.build_dataframe()
        gsw_zero = gsw_zero.iloc[(:, 0:30)].copy()
        gsw_zero = gsw_zero.reindex(index=gsw_zero.index[::(- 1)])
        start_date = gsw_zero.index[0]
        fred_data = web.DataReader(['DFF', 'DTB3', 'DTB6'], 'fred', start_date)
        zero_yld_matrix = pd.concat([fred_data.dropna(), gsw_zero], axis=1)
        zero_yld_matrix = zero_yld_matrix.fillna(method='ffill')
        write_feather(zero_yld_matrix, str((self.DB_PATH / 'fedzero.feather')))
        end_time = time()
        print((('File updated in ' + str(round((end_time - start_time)))) + ' seconds'))
    except:
        raise Exception('Zero curve update failed - Zero curve not updated')
