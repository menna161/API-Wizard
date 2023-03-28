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


def _create_from_refund(self, debit_note, refund, account, bucket):
    'Internal function used to create the credit note from\n           the passed refund. This will actually transfer value from the\n           debit note to the credited account (which was the original\n           debited account)\n\n           debit_note (DebitNote): DebitNote to use\n           refund (Refund): Refund from which to take value to create\n           CreditNote\n           account (Account): Account to credit refund to\n           bucket (Bucket): Bucket to load data from\n\n           Returns:\n                None\n        '
    from Acquire.Accounting import DebitNote as _DebitNote
    from Acquire.Accounting import Refund as _Refund
    from Acquire.Accounting import TransactionRecord as _TransactionRecord
    from Acquire.Accounting import TransactionState as _TransactionState
    from Acquire.Accounting import Account as _Account
    if (not isinstance(debit_note, _DebitNote)):
        raise TypeError('You can only create a CreditNote with a DebitNote')
    if (not isinstance(refund, _Refund)):
        raise TypeError(('You can only refund a Refund object: %s' % str(refund.__class__)))
    transaction = _TransactionRecord.load_test_and_set(refund.transaction_uid(), _TransactionState.REFUNDING, _TransactionState.REFUNDING, bucket=bucket)
    transaction.assert_matching_refund(refund)
    if (account is None):
        account = _Account(transaction.debit_account_uid(), bucket)
    elif (account.uid() != refund.debit_account_uid()):
        raise ValueError(('The accounts do not match when refunding the receipt: %s versus %s' % (account.uid(), refund.debit_account_uid())))
    (uid, datetime) = account._credit_refund(debit_note, refund, bucket)
    self._account_uid = account.uid()
    self._debit_account_uid = debit_note.account_uid()
    self._datetime = datetime
    self._uid = uid
    self._debit_note_uid = debit_note.uid()
    self._value = debit_note.value()
    self._is_provisional = debit_note.is_provisional()
    if self._is_provisional:
        self._receipt_by = debit_note.receipt_by()
    _TransactionRecord.load_test_and_set(refund.transaction_uid(), _TransactionState.REFUNDING, _TransactionState.REFUNDED, bucket=bucket)
