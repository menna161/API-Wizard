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


def receipt_by(self):
    'Return the datetime by which this credit note must be\n           receipted, or else the funds will be returned. This will\n           return None if the CreditNote does not need receipting\n\n           Returns:\n                datetime: Date by which the credit note must be receipted\n        '
    if self.is_provisional():
        return self._receipt_by
    else:
        return None
