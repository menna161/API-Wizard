import datetime
import re
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from aao.spiders.spider import Spider
from aao.spiders import sports


def _parse_datetime(self, row):
    format_ = '%a %d %b'
    date = datetime.date.today()
    while (date.strftime(format_) != row[0]):
        date += datetime.timedelta(1)
    time = datetime.datetime.strptime(row[1], '%H:%M').time()
    return datetime.datetime.combine(date, time)
