import datetime
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from aao.spiders.spider import Spider
from aao.spiders import sports


def _parse_datetime(self, row):
    if (row[0] in {'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'}):
        format_ = '%a'
    else:
        row[0] = ' '.join(row[0].split(' ')[:2])
        format_ = '%-e %b'
    date = datetime.date.today()
    while (date.strftime(format_) != row[0]):
        date += datetime.timedelta(1)
    time = datetime.datetime.strptime(row[1], '%H:%M').time()
    return datetime.datetime.combine(date, time)
