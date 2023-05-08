import requests
import pytz
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from utils import _setup_debug_logger


def get_day_based_on_tz(day, tz):
    'Gets the client date() based on tz passed as parameter.\n    '
    server_day = datetime.now(tz=pytz.timezone(SERVER_TIMEZONE))
    if ((tz is not None) and (tz in pytz.all_timezones)):
        client_day = server_day.astimezone(pytz.timezone(tz)).date()
        asked = TIMEDELTA_DAYS[day]
        asked_date = (client_day + timedelta(days=asked))
        if (asked_date > server_day.date()):
            day = 'tomorrow'
        elif (asked_date < server_day.date()):
            day = 'yesterday'
        elif ((asked == (- 1)) and (asked_date == server_day.date())):
            day = 'today'
    return day
