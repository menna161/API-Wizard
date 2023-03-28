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


@staticmethod
def from_data(data):
    'Construct and return a new CreditNote from the passed json-decoded\n            dictionary\n\n            Args:\n                data (dict): JSON serialised dictionary of object\n            Returns:\n                CreditNote: CreditNote created from JSON data\n        '
    note = CreditNote()
    if (data and (len(data) > 0)):
        from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
        from Acquire.Accounting import create_decimal as _create_decimal
        note._account_uid = data['account_uid']
        note._debit_account_uid = data['debit_account_uid']
        note._uid = data['uid']
        note._debit_note_uid = data['debit_note_uid']
        note._datetime = _string_to_datetime(data['datetime'])
        note._value = _create_decimal(data['value'])
        note._is_provisional = data['is_provisional']
        if note._is_provisional:
            note._receipt_by = _string_to_datetime(data['receipt_by'])
    return note
