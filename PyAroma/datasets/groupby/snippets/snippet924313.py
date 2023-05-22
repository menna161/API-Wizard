import pandas as pd
import numpy as np


def watch_month_plot(watch: pd.DataFrame):
    df = pd.DataFrame()
    df['time'] = watch['time']
    df['amount'] = 1
    df = df.groupby(df['time'].dt.month).sum()
    df = df.reindex(range(1, 13)).fillna(0)
    df.index = df.index.map((lambda x: calendar.month_abbr[x]))
    plot = df.plot(kind='bar', color=COLOR)
    plot.set_title('Videos watched per month')
    plot.set_ylabel('')
    plot.set_xlabel('')
    plot.get_legend().remove()
    return plot
