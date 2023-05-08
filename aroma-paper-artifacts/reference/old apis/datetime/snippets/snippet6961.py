from Acquire.Accounting import DebitNote as _DebitNote
from Acquire.Accounting import Refund as _Refund
from Acquire.Accounting import TransactionRecord as _TransactionRecord
from Acquire.Accounting import TransactionState as _TransactionState
from Acquire.Accounting import Account as _Account
from Acquire.Accounting import DebitNote as _DebitNote
from Acquire.Accounting import Refund as _Refund
from Acquire.Accounting import TransactionRecord as _TransactionRecord
from Acquire.Accounting import TransactionState as _TransactionState
from Acquire.Accounting import Account as _Account
from Acquire.Accounting import Receipt as _Receipt
from Acquire.Accounting import DebitNote as _DebitNote
from Acquire.Accounting import Account as _Account
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Accounting import create_decimal as _create_decimal


def __init__(self, debit_note=None, account=None, receipt=None, refund=None, bucket=None):
    'Create the corresponding credit note for the passed debit_note. This\n           will credit value from the note to the passed account. The credit\n           will use the same UID as the debit, and the same datetime. This\n           will then be paired with the debit note to form a TransactionRecord\n           that can be written to the ledger\n        '
    self._account_uid = None
    nargs = ((receipt is not None) + (refund is not None))
    if (nargs > 1):
        raise ValueError('You can create a CreditNote with a receipt or a refund - not both!')
    if (receipt is not None):
        self._create_from_receipt(debit_note, receipt, account, bucket)
    elif (refund is not None):
        self._create_from_refund(debit_note, refund, account, bucket)
    elif ((debit_note is not None) and (account is not None)):
        self._create_from_debit_note(debit_note, account, bucket)
    else:
        self._debit_account_uid = None
        self._datetime = None
        self._uid = None
        self._debit_note_uid = None
        from Acquire.Accounting import create_decimal as _create_decimal
        self._value = _create_decimal(0)
