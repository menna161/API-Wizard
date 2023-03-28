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


def _create_from_receipt(self, debit_note, receipt, account, bucket):
    'Internal function used to create the credit note from\n           the passed receipt. This will actually transfer value from the\n           debit note to the credited account\n\n           debit_note (DebitNote): DebitNote from which to take value\n           receipt (Receipt): Receipt to create CreditNote from\n           account (Account): Account to credit\n           bucket (Bucket): Bucket to load data from\n\n           Returns:\n                None\n\n        '
    from Acquire.Accounting import DebitNote as _DebitNote
    from Acquire.Accounting import Refund as _Refund
    from Acquire.Accounting import TransactionRecord as _TransactionRecord
    from Acquire.Accounting import TransactionState as _TransactionState
    from Acquire.Accounting import Account as _Account
    from Acquire.Accounting import Receipt as _Receipt
    if (not isinstance(debit_note, _DebitNote)):
        raise TypeError('You can only create a CreditNote with a DebitNote')
    if (not isinstance(receipt, _Receipt)):
        raise TypeError(('You can only receipt a Receipt object: %s' % str(receipt.__class__)))
    transaction = _TransactionRecord.load_test_and_set(receipt.transaction_uid(), _TransactionState.RECEIPTING, _TransactionState.RECEIPTING, bucket=bucket)
    transaction.assert_matching_receipt(receipt)
    if (account is None):
        account = _Account(transaction.credit_account_uid(), bucket)
    elif (account.uid() != receipt.credit_account_uid()):
        raise ValueError(('The accounts do not match when crediting the receipt: %s versus %s' % (account.uid(), receipt.credit_account_uid())))
    (uid, datetime) = account._credit_receipt(debit_note, receipt, bucket)
    self._account_uid = account.uid()
    self._debit_account_uid = debit_note.account_uid()
    self._datetime = datetime
    self._uid = uid
    self._debit_note_uid = debit_note.uid()
    self._value = debit_note.value()
    self._is_provisional = debit_note.is_provisional()
    if debit_note.is_provisional():
        self._receipt_by = debit_note.receipt_by()
    _TransactionRecord.load_test_and_set(receipt.transaction_uid(), _TransactionState.RECEIPTING, _TransactionState.RECEIPTED, bucket=bucket)
