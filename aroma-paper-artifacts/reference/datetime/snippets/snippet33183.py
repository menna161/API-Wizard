import logging
from lxml import etree
from lxml.builder import ElementMaker
from datetime import datetime
from pytz import utc
from ..exceptions import FailedExchangeException


def _parse_date(self, date_string):
    date = datetime.strptime(date_string, self.EXCHANGE_DATE_FORMAT)
    date = date.replace(tzinfo=utc)
    return date
