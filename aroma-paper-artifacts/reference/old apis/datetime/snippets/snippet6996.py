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


def _create_from_refund(self, refund, account, bucket):
    'Function used to construct a debit note by extracting\n           the value specified in the passed refund from the specified\n           account. This is authorised using the authorisation held in\n           the refund. Note that the refund must match\n           up with a prior existing provisional transaction, and this\n           must not have already been refunded. This will\n           actually take value out of the passed account, with that\n           value residing in this debit note until it is credited to\n           another account\n\n           Args:\n                refund (Refund): Refund to create debit note from\n                account (Account):\n        '
    from Acquire.Accounting import Refund as _Refund
    if (not isinstance(refund, _Refund)):
        raise TypeError('You can only create a DebitNote with a Refund')
    if refund.is_null():
        return
    if (bucket is None):
        from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
        bucket = _get_service_account_bucket()
    from Acquire.Accounting import TransactionRecord as _TransactionRecord
    from Acquire.Accounting import TransactionState as _TransactionState
    from Acquire.Accounting import Account as _Account
    transaction = _TransactionRecord.load_test_and_set(refund.transaction_uid(), _TransactionState.DIRECT, _TransactionState.REFUNDING, bucket=bucket)
    try:
        transaction.assert_matching_refund(refund)
        if (account is None):
            account = _Account(transaction.credit_account_uid(), bucket)
        elif (account.uid() != refund.credit_account_uid()):
            raise ValueError(('The accounts do not match when debiting the refund: %s versus %s' % (account.uid(), refund.credit_account_uid())))
        (uid, datetime) = account._debit_refund(refund, bucket)
        self._transaction = refund.transaction()
        self._account_uid = refund.credit_account_uid()
        self._authorisation = refund.authorisation()
        self._is_provisional = False
        self._datetime = datetime
        self._uid = str(uid)
    except:
        _TransactionRecord.load_test_and_set(refund.transaction_uid(), _TransactionState.REFUNDING, _TransactionState.DIRECT)
        raise
