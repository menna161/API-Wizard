import pandas as pd
import numpy as np
import pyfolio as pf
from option_utilities import get_actual_option_expiries, USZeroYieldCurve, get_theoretical_strike, read_feather
from spx_data_update import UpdateSP500Data, get_dates


@property
def performance_summary(self):
    'Get simulation performance'
    performance = pf.timeseries.perf_stats(self.returns)
    perf_index = list(performance.index)
    performance = performance['perf_stats']
    (performance['StartDate'], performance['EndDate']) = list(self.simulation_parameters.sim_dates_live[[0, (- 1)]].strftime('%b %d, %Y'))
    (performance['Leverage'], performance['ZScore'], performance['Avg_Days']) = [self.leverage.mean(), self.simulation_parameters.zscore, self.days_2_expiry.mean()]
    performance = performance.reindex((['StartDate', 'EndDate', 'Leverage', 'ZScore', 'Avg_Days'] + perf_index))
    performance = performance.append(self.greeks.mean())
    performance = performance.rename(self.strategy_name)
    performance = performance.to_frame()
    performance = performance.drop(['active_underlying_price_1545'], axis=0)
    return performance
