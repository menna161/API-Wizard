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


@staticmethod
def from_data(data):
    'Return a DebitNote that has been extracted from the passed\n           json-decoded dictionary\n\n           Args:\n                data (dict): Dictionary from which to create object\n           Returns:\n                DebitNote: Created from dictionary\n        '
    d = DebitNote()
    if (data and (len(data) > 0)):
        from Acquire.Accounting import Transaction as _Transaction
        from Acquire.Identity import Authorisation as _Authorisation
        from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
        d._transaction = _Transaction.from_data(data['transaction'])
        d._account_uid = data['account_uid']
        d._authorisation = _Authorisation.from_data(data['authorisation'])
        d._is_provisional = data['is_provisional']
        d._datetime = _string_to_datetime(data['datetime'])
        d._uid = data['uid']
        if d._is_provisional:
            d._receipt_by = _string_to_datetime(data['receipt_by'])
    return d
