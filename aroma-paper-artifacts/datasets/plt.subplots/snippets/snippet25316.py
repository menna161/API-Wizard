from option_utilities import read_feather, write_feather
from spx_data_update import UpdateSP500Data, IbWrapper
from ib_insync import IB, Index, util
import numpy as np
import pandas as pd
from arch import arch_model
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def plot_vol_forecast(self, num_days=10):
    expected_volatility = self.expected_vol
    (fig, ax) = plt.subplots(figsize=(12, 5), dpi=80, facecolor='w', edgecolor='k')
    for i in range((- 1), (- (num_days + 1)), (- 1)):
        if (i == (- 1)):
            expected_volatility.iloc[(:, (- 1))].plot(color='r')
        else:
            c = cm.viridis(((- i) / num_days), 1)
            expected_volatility.iloc[(:, i)].plot(color=c)
    plt.autoscale(enable=True, axis='x', tight=True)
    legend_labels = expected_volatility.iloc[(:, (- num_days):)].columns.strftime('%d-%b')
    _ = plt.legend(legend_labels[::(- 1)])
    _ = plt.title('HAR Volatity Forecast')
    _ = ax.set_ylabel('Annualized Vol %')
    return ax
