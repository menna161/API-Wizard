import datetime
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from aao.spiders.spider import Spider
from aao.spiders import sports


def _parse_datetime(self, row):
    (month, day, year) = row[0].split(' - ')[(- 1)].split('/')
    date = datetime.date(int(year), int(month), int(day))
    try:
        time = datetime.datetime.strptime(row[1], '%I:%M %p').time()
    except ValueError:
        if ('+' in row[1]):
            row.pop(1)
        time_str = ' '.join(row[1].split(' ')[(- 2):])
        time = datetime.datetime.strptime(time_str, '%I:%M %p').time()
    return datetime.datetime.combine(date, time)
