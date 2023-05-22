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


def _create_from_transaction(self, transaction, account, authorisation, authorisation_resource, is_provisional, receipt_by, bucket):
    "Function used to construct a debit note by extracting the\n           specified transaction value from the passed account. This\n           is authorised using the passed authorisation, and can be\n           a provisional debit if 'is_provisional' is true. This will\n           actually take value out of the passed account, with that\n           value residing in this debit note until it is credited\n           to another account\n\n           Args:\n                transaction (Transaction): Transaction that holds the value\n                to be used\n                account (Account): Account to take value from\n                authorisation (Authorisation): Authorises the removal\n                of value from account\n                is_provisional (bool): Whether the debit is provisional or not\n                receipt_by (datetime): Datetime by which debit must be\n                receipted\n                bucket (dict): Bucket to read data from\n        "
    from Acquire.Accounting import Transaction as _Transaction
    from Acquire.Accounting import Account as _Account
    if (not isinstance(transaction, _Transaction)):
        raise TypeError('You can only create a DebitNote with a Transaction')
    if (not isinstance(account, _Account)):
        raise TypeError('You can only create a DebitNote with a valid Account')
    if (authorisation is not None):
        from Acquire.Identity import Authorisation as _Authorisation
        if (not isinstance(authorisation, _Authorisation)):
            raise TypeError('Authorisation must be of type Authorisation')
    self._transaction = transaction
    self._account_uid = account.uid()
    self._authorisation = authorisation
    self._is_provisional = is_provisional
    (uid, datetime, receipt_by) = account._debit(transaction=transaction, authorisation=authorisation, authorisation_resource=authorisation_resource, is_provisional=is_provisional, receipt_by=receipt_by, bucket=bucket)
    from Acquire.ObjectStore import datetime_to_datetime as _datetime_to_datetime
    self._datetime = _datetime_to_datetime(datetime)
    self._uid = str(uid)
    if is_provisional:
        assert (receipt_by is not None)
        self._receipt_by = receipt_by
    else:
        assert (receipt_by is None)
