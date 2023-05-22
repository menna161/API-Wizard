import pandas as pd
import numpy as np


def watch_week_plot(watch: pd.DataFrame):
    df = pd.DataFrame()
    df['time'] = watch['time']
    df['amount'] = 1
    df = df.groupby(df['time'].dt.dayofweek).sum()
    df = df.reindex(range(0, 7)).fillna(0)
    df.index = df.index.map((lambda x: calendar.day_abbr[x]))
    plot = df.plot(kind='bar', color=COLOR)
    plot.set_title('Videos watched per weekday')
    plot.set_ylabel('')
    plot.set_xlabel('')
    plot.get_legend().remove()
    return plot
