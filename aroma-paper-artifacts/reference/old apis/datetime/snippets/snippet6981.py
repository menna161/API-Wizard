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


def to_data(self):
    'Return this credit note as a dictionary that can be\n           encoded to JSON\n\n           Returns:\n                dict: Dictionary of object to be encoded to JSON\n        '
    data = {}
    if (not self.is_null()):
        from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
        data['account_uid'] = self._account_uid
        data['debit_account_uid'] = self._debit_account_uid
        data['uid'] = self._uid
        data['debit_note_uid'] = self._debit_note_uid
        data['datetime'] = _datetime_to_string(self._datetime)
        data['value'] = str(self._value)
        data['is_provisional'] = self._is_provisional
        if self._is_provisional:
            data['receipt_by'] = _datetime_to_string(self._receipt_by)
    return data
