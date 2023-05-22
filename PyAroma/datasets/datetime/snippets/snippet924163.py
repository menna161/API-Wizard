import numpy as np
from datetime import datetime
from scipy import sparse


def timestamp_delta_generator(days=0, months=0, years=0):
    days_delta_timestamp_unit = date_subtractor(datetime(2006, 1, 1), datetime(2006, 1, 2))
    months_delta_timestamp_unit = date_subtractor(datetime(2006, 1, 1), datetime(2006, 2, 1))
    years_delta_timestamp_unit = date_subtractor(datetime(2006, 1, 1), datetime(2007, 1, 1))
    return (((days * days_delta_timestamp_unit) + (months * months_delta_timestamp_unit)) + (years_delta_timestamp_unit * years))
