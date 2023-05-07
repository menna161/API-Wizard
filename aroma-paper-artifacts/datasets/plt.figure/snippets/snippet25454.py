import pyfolio as pf
import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARMA
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import scipy.stats as scs
import matplotlib.gridspec as gridspec
from ib_insync import Future, util
import matplotlib as mpl
import matplotlib.pyplot as plt
import os
import re
import zipfile
from option_utilities import read_feather
from pyfolio.timeseries import cum_returns
from spx_data_update import UpdateSP500Data, ImpliedVolatilityHistory, SP500Index, IbWrapper, GetRawCBOEOptionData
from option_utilities import PlotConstants, chart_format


def plot_rolling_beta(self, **kwargs):
    (beta, rolling_window) = self.vix_beta(**kwargs)
    pc = PlotConstants()
    with plt.style.context('bmh'):
        _ = plt.figure(figsize=pc.fig_size, dpi=600, facecolor='None', edgecolor='None')
        gs = gridspec.GridSpec(1, 1, wspace=0.5, hspace=0.25)
        ax_beta = plt.subplot(gs[:])
        ax_beta = beta.plot(lw=1.5, ax=ax_beta, grid=True, alpha=0.4, color=pc.color_yellow, title='VIX beta to S&P500 - {} days rolling window'.format(rolling_window))
        ax_beta.set_ylabel('Beta')
        ax_beta.axhline(beta.mean(), color='k', ls='--', lw=0.75, alpha=1.0)
        chart_format([ax_beta], pc.color_light)
        plt.autoscale(enable=True, axis='x', tight=True)
    return ax_beta
