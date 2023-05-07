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


def plot_performance_quad(returns, fig_path=None, fig_name='heat_map_quad', font_size=20):

    def truncate_colormap(cmap, minval=0.0, maxval=1.0, n=100):
        new_cmap = colors.LinearSegmentedColormap.from_list('trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval), cmap(np.linspace(minval, maxval, n)))
        return new_cmap
    fig = plt.figure(figsize=(16, 9))
    fig.suptitle(returns.name, fontsize=16)
    gs = gridspec.GridSpec(2, 2, wspace=0.2, hspace=0.3)
    ax_heatmap = plt.subplot(gs[(0, 0)])
    ax_monthly = plt.subplot(gs[(0, 1)])
    ax_box_plot = plt.subplot(gs[(1, 0)])
    ax_yearly = plt.subplot(gs[(1, 1)])
    monthly_ret_table = pf.timeseries.aggregate_returns(returns, 'monthly')
    monthly_ret_table = monthly_ret_table.unstack().round(3)
    ax = plt.gca()
    cmap = cm.viridis
    new_cmap = truncate_colormap(cmap, 0.2, 0.8)
    sns.heatmap((monthly_ret_table.fillna(0) * 100.0), annot=True, annot_kws={'size': font_size}, alpha=1.0, center=0.0, cbar=False, mask=monthly_ret_table.isna(), cmap=new_cmap, ax=ax_heatmap)
    ax_heatmap.set_xticklabels(np.arange(0.5, 12.5, step=1))
    ax_heatmap.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)
    ylabels = ax_heatmap.get_yticklabels()
    ax_heatmap.set_yticklabels(ylabels, rotation=45)
    ax_heatmap.set_xlabel('')
    ax_heatmap.set_ylabel('')
    pf.plotting.plot_monthly_returns_dist(returns, ax=ax_monthly)
    ax_monthly.xaxis.set_major_formatter(FormatStrFormatter('%.1f%%'))
    ax_monthly.set_xlabel('')
    leg1 = ax_monthly.legend(['mean'], framealpha=0.0, prop={'size': font_size})
    for text in leg1.get_texts():
        text.set_label('mean')
    df_weekly = pf.timeseries.aggregate_returns(returns, convert_to='weekly')
    df_monthly = pf.timeseries.aggregate_returns(returns, convert_to='monthly')
    pf.plotting.plot_return_quantiles(returns, df_weekly, df_monthly, ax=ax_box_plot)
    pf.plotting.plot_annual_returns(returns, ax=ax_yearly)
    _ = ax_yearly.legend(['mean'], framealpha=0.0, prop={'size': font_size})
    ax_yearly.xaxis.set_major_formatter(FormatStrFormatter('%.1f%%'))
    plt.xticks(rotation=45)
    ax_yearly.set_xlabel('')
    ax_yearly.set_ylabel('')
    for ax in [ax_box_plot, ax_heatmap, ax_monthly, ax_yearly]:
        for item in (([ax.title, ax.xaxis.label, ax.yaxis.label] + ax.get_xticklabels()) + ax.get_yticklabels()):
            item.set_fontsize(font_size)
    for items in (ax_yearly.get_yticklabels() + ax_heatmap.get_yticklabels()):
        items.set_fontsize((font_size - 5))
    if (fig_path is not None):
        if Path.is_dir(fig_path):
            plt.savefig((fig_path / fig_name), dpi=600, bbox_inches='tight', transparent=True)
        return fig
