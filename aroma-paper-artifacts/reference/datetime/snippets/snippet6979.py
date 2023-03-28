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


def _create_from_debit_note(self, debit_note, account, bucket):
    'Internal function used to create the credit note that matches\n           the passed debit note. This will actually transfer value from\n           the debit note to the passed account\n\n           debit_note (DebitNote): DebitNote to take value from\n           account (Account): Account to credit\n           bucket (Bucket): Bucket to load data from\n\n           Returns:\n                None\n        '
    from Acquire.Accounting import DebitNote as _DebitNote
    from Acquire.Accounting import Account as _Account
    if (not isinstance(debit_note, _DebitNote)):
        raise TypeError('You can only create a CreditNote with a DebitNote')
    if (not isinstance(account, _Account)):
        raise TypeError('You can only create a CreditNote with an Account')
    (uid, datetime) = account._credit(debit_note, bucket=bucket)
    self._account_uid = account.uid()
    self._debit_account_uid = debit_note.account_uid()
    self._datetime = datetime
    self._uid = uid
    self._debit_note_uid = debit_note.uid()
    self._value = debit_note.value()
    self._is_provisional = debit_note.is_provisional()
    if self._is_provisional:
        self._receipt_by = debit_note.receipt_by()
