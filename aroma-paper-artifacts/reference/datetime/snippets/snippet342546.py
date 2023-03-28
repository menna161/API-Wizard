import matplotlib.pyplot as plt
import streamlit as st
from pandas import infer_freq
from statsmodels.tsa.seasonal import seasonal_decompose


def decompose_series(ts):
    '\n    This function applies a seasonal decomposition to a time series. It will generate a season plot, a trending plot, and, finally, a resid plot\n\n    Args.\n        ts (Pandas Series): a time series to be decomposed\n    '
    fig = plt.Figure(figsize=(12, 7))
    ax1 = plt.subplot(311)
    ax2 = plt.subplot(312)
    ax3 = plt.subplot(313)
    try:
        decomposition = seasonal_decompose(ts)
    except AttributeError:
        error_message = "\n                        Seems that your DATE column is not in a proper format. \n                        Be sure that it's in a valid format for a Pandas to_datetime function.\n                        "
        raise AttributeError(error_message)
    decomposition.seasonal.plot(color='green', ax=ax1, title='Seasonality')
    plt.legend('')
    decomposition.trend.plot(color='green', ax=ax2, title='Trending')
    plt.legend('')
    decomposition.resid.plot(color='green', ax=ax3, title='Resid')
    plt.legend('')
    plt.subplots_adjust(hspace=1)
    st.pyplot()
