from datetime import datetime
from unittest import TestCase
from freezegun import freeze_time
from nubank_sync_ynab import util


def test_parse_transaction_date(self):
    transaction = {'time': '2017-06-21T10:00:00Z'}
    parsed = util.parse_transaction_date(transaction)
    self.assertEqual(parsed, datetime(2017, 6, 21).date())
