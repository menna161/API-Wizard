import json
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from graph_utils import dates_to_today


def in_date_set(date_set, check_date):
    'Checks whether check_date is within any of the bounds in date_set'
    check_month = datetime(year=check_date.year, month=check_date.month, day=1).date()
    for pair in date_set:
        p0 = datetime.strptime(pair[0], '%Y-%m-%d').date()
        p1 = datetime.strptime(pair[1], '%Y-%m-%d').date()
        if (p0 <= check_month <= p1):
            return True
    return False
