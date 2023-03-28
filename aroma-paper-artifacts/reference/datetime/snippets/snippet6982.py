from Acquire.Accounting import Refund as _Refund
from Acquire.Accounting import TransactionRecord as _TransactionRecord
from Acquire.Accounting import TransactionState as _TransactionState
from Acquire.Accounting import Account as _Account
from Acquire.Accounting import Receipt as _Receipt
from Acquire.Accounting import TransactionRecord as _TransactionRecord
from Acquire.Accounting import TransactionState as _TransactionState
from Acquire.Accounting import Account as _Account
from Acquire.Accounting import Transaction as _Transaction
from Acquire.Accounting import Account as _Account
from Acquire.ObjectStore import datetime_to_datetime as _datetime_to_datetime
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Identity import Authorisation as _Authorisation
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Accounting import Transaction as _Transaction
from Acquire.Identity import Authorisation as _Authorisation
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime


def __init__(self, transaction=None, account=None, authorisation=None, is_provisional=False, receipt_by=None, receipt=None, refund=None, authorisation_resource=None, bucket=None):
    "Create a debit note for the passed transaction will debit value\n           from the passed account. The note will create a unique ID (uid)\n           for the debit, plus the datetime of the time that value was drawn\n           from the debited account. This debit note will be paired with a\n           corresponding credit note from the account that received the value\n           from the transaction so that a balanced TransactionRecord can be\n           written to the ledger. If the note is provisional, then the value\n           of the transaction will be held until the corresponding CreditNote\n           has been receipted. This must be receipted before 'receipt_by',\n           else the value will be returned to the DebitNote account\n           (it will be automatically refunded)\n        "
    self._transaction = None
    nargs = (((transaction is not None) + (refund is not None)) + (receipt is not None))
    if (nargs > 1):
        raise ValueError('You can only choose to create a debit note from a transaction, receipt or refund!')
    if (refund is not None):
        self._create_from_refund(refund, account, bucket)
    elif (receipt is not None):
        self._create_from_receipt(receipt, account, bucket)
    elif (transaction is not None):
        if (account is None):
            raise ValueError('You need to supply the account from which the transaction will be taken')
        self._create_from_transaction(transaction=transaction, account=account, authorisation=authorisation, authorisation_resource=authorisation_resource, is_provisional=is_provisional, receipt_by=receipt_by, bucket=bucket)
