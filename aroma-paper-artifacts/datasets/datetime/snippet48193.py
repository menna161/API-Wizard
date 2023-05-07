from datetime import datetime
from unittest import TestCase
from pynYNAB.schema import Catalog, Budget, Payee, Transaction
from nubank_sync_ynab.ynab import YNAB


def test_add_transaction(self):
    self.ynab.add_transaction(payee='John Snow', date=datetime(2017, 6, 21).date(), id='001', value=10.0, subcategory='Bla Bla')
    self.assertEqual(self.ynab.delta, 3)
    self.ynab.add_transaction(payee='John Snow', date=datetime(2017, 6, 21).date(), id='001', value=10.0, subcategory='Bla Bla')
    self.assertEqual(self.ynab.delta, 3)
