from numpy import isscalar
from pandas import DatetimeIndex, date_range, merge
from streamlit import warning
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm


def test_time_series(ts):
    '\n    This function will test the transformed time series with a decomposition and a model training. \n    This will ensure that the data a proper format to be used in the rest of the project. This is a crucial\n    step to understand if the time series has a valid datetime index (used by decomposition function and ARIMA)\n    '
    seasonal_decompose(ts)
    mod = sm.tsa.statespace.SARIMAX(ts, order=(0, 0, 1))
    results = mod.fit()
    assert (not isscalar(results.forecast(10).index[0])), 'The forecasts index is not a datetime type'
