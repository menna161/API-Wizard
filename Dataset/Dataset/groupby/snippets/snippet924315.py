import pandas as pd
import numpy as np


def watch_hour_plot(watch: pd.DataFrame):
    df = pd.DataFrame()
    df['time'] = watch['time']
    df['amount'] = 1
    df = df.groupby(df['time'].dt.hour).sum()
    df = df.reindex(range(0, 24)).fillna(0)
    df.index = df.index.map((lambda x: f'{x:02}:00'))
    plot = df.plot(kind='bar', color=COLOR)
    plot.set_title('Videos watched per hour')
    plot.set_ylabel('')
    plot.set_xlabel('')
    plot.get_legend().remove()
    return plot
