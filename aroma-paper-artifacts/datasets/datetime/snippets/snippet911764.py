import datetime
import json
import os
import re
import pygraphviz as pgv


def dates_to_today(start_year):
    'Generate a list of dates from the beginning of start_year to the current date'
    today = datetime.date.today()
    dates = []
    for year in range(start_year, (today.year + 1)):
        for month in range(1, 13):
            date = datetime.date(year, month, 1)
            if (date > today):
                return dates
            dates.append(date)
    return dates
