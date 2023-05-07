import pandas as pd
import numpy as np
import pyfolio as pf
from option_utilities import get_actual_option_expiries, USZeroYieldCurve, get_theoretical_strike, read_feather
from spx_data_update import UpdateSP500Data, get_dates


def csv_2_feather(csv_directory):
    spxw_feather = (UpdateSP500Data.TOP_LEVEL_PATH / 'raw_df.feather')
    history = pd.read_feather(spxw_feather)
    last_date = pd.DatetimeIndex(history['quote_date'].unique()).sort_values()[(- 1)]
    csv_dates = get_dates(csv_directory, file_type='.csv')
    csv_dates = csv_dates.to_series()
    csv_dates = csv_dates[(csv_dates > last_date)]
    csv_dates = csv_dates.index
    try:
        file_list = []
        for item in csv_dates:
            file_list.append((('UnderlyingOptionsEODCalcs_' + item.strftime('%Y-%m-%d')) + '.csv'))
        dataframe_list = []
        greek_cols = ['delta_1545', 'rho_1545', 'vega_1545', 'gamma_1545', 'theta_1545']
        for item in file_list:
            if item.endswith('.csv'):
                future_df = pd.read_csv((csv_directory / item))
                if (pd.DatetimeIndex(future_df['quote_date'].unique()) > last_date):
                    dataframe_list.append(future_df)
        raw_df = pd.concat(dataframe_list, axis=0, ignore_index=True)
        raw_df = raw_df[['quote_date', 'root', 'expiration', 'strike', 'option_type', 'open', 'high', 'low', 'close', 'active_underlying_price_1545', 'implied_volatility_1545', 'delta_1545', 'gamma_1545', 'theta_1545', 'vega_1545', 'rho_1545', 'bid_1545', 'ask_1545']]
        raw_df = raw_df[(raw_df['root'] == 'SPXW')]
        raw_df.loc[(:, ['quote_date', 'expiration'])] = raw_df.loc[(:, ['quote_date', 'expiration'])].apply(pd.to_datetime)
        raw_df.loc[(:, greek_cols)] = raw_df.loc[(:, greek_cols)].apply(pd.to_numeric, errors='coerce')
        raw_df = pd.concat([history, raw_df], axis=0)
        raw_df = raw_df.sort_values('quote_date').reset_index(drop=True)
        raw_df.to_feather(spxw_feather)
        print('Feather updated')
    except ValueError:
        print('Feather file not updated')
        raw_df = history
    return raw_df
