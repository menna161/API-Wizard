from datetime import datetime
from dateutil.relativedelta import relativedelta
from hive.utils.normalize import rep_to_raw


def last_month():
    'Get the date 1 month ago.'
    return (datetime.now() + relativedelta(months=(- 1)))
