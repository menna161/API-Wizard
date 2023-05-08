from numpy import isscalar
from pandas import DatetimeIndex, date_range, merge
from streamlit import warning
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm


def transform_time_series(df, ds_column, date_frequency, y):
    '\n    Transforms a Pandas DataFrame into a Pandas Series, using a column as the index\n\n    Args:\n        df (Pandas DataFrame): a DataFrame to be transformed\n        ds_column (str): column name that will be used as an index\n        date_frequency (str): the frequency of the dataset. It could be daily, monthly, etc.\n\n    Return:\n        df (Pandas Series): transformed DataFrame\n    '
    date_frequency_dict = {'Hourly': 'H', 'Daily': 'D', 'Monthly': 'MS', 'Quarterly': 'Q', 'Yearly': 'Y'}
    df.set_index(ds_column, inplace=True)
    df = df.dropna()
    try:
        df.index = df.index.astype('datetime64[ns]')
        test_time_series(df[y])
    except:
        try:
            date_format = DatetimeIndex(df.index[(- 10):], freq='infer')
            df.index = df.asfreq(date_format.freq, fill_value=0)
            test_time_series(df[y])
        except ValueError:
            try:
                fill_date_range = date_range(df.index.min(), df.index.max(), freq=date_format.freq)
                df = merge(fill_date_range.to_frame().drop(0, axis=1), df, how='left', right_index=True, left_index=True)
                null_values = df[df.loc[:, y].isnull()].index.values
                if (len(null_values) > 0):
                    warning('We found null values at {}. Filling it with zeros.'.format(null_values))
                    df = df.fillna(0)
                test_time_series(df[y])
            except:
                try:
                    warning_message = '\n                                We could not find the proper date frequency of this dataset. \n                                We will try to infer it based on the FREQUENCY field on the sidebar, but be sure that\n                                this dataset is in one of the following formats (Hourly, Daily, Monthly, Quarterly, or Yearly)\n                                '
                    warning(warning_message)
                    df = df.asfreq(date_frequency_dict[date_frequency])
                    null_values = df[df.loc[:, y].isnull()].index.values
                    if (len(null_values) > 0):
                        warning('We found null values at {}. Filling it with zeros.'.format(null_values))
                        df = df.fillna(0)
                    test_time_series(df[y])
                except:
                    error_message = '\n                                    There was a problem while we tried to convert the DATE column for a valid format.\n                                    Be sure there is no null value in the DATE column and that it is in a valid format for Pandas to_datetime function. \n                                    Please, refer to (https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases) to know more abbout the\n                                    date frequencies\n                                    '
                    raise TypeError(error_message)
    return df
