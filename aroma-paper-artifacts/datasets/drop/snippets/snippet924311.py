import pandas as pd
import numpy as np


def creator_plot(watch: pd.DataFrame, number: int):
    df = watch['channel'].value_counts()
    df.drop(['unknown'], inplace=True)
    df = df.head(number).sort_values()
    plot = df.plot(kind='barh', color=COLOR, figsize=[6.4, (number * 0.28)])
    plot.set_xlabel('videos watched')
    plot.set_title(f'Top {number} creators')
    return plot
