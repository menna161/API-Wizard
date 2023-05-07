import datetime
import logging
from pynYNAB.ClientFactory import nYnabClientFactory
from pynYNAB.connection import nYnabConnection
from pynYNAB.schema.budget import Account, Transaction, Payee


def add_transaction(self, **kwargs):
    logging.info('Adding transaction')
    payee = self.get_payee(kwargs['payee'])
    subcategory = self.get_subcategory(kwargs['subcategory'])
    if (not self.has_matching_transaction(kwargs['id'])):
        logging.info('Creating transaction')
        transaction = Transaction()
        transaction.date = kwargs['date']
        transaction.memo = 'AUTO IMPORT - {}'.format(kwargs['id'])
        transaction.imported_payee = payee.name
        transaction.entities_payee_id = payee.id
        transaction.entities_subcategory_id = (subcategory.id if subcategory else None)
        transaction.imported_date = datetime.datetime.now().date()
        transaction.source = 'Imported'
        transaction.amount = kwargs['value']
        transaction.entities_account_id = self.account.id
        self.client.budget.be_transactions.append(transaction)
        self.delta += 1
