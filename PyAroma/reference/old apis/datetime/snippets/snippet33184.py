import logging
from lxml import etree
from lxml.builder import ElementMaker
from datetime import datetime
from pytz import utc
from ..exceptions import FailedExchangeException


def _parse_date_only_naive(self, date_string):
    date = datetime.strptime(date_string[0:10], self.EXCHANGE_DATE_FORMAT[0:8])
    return date.date()
