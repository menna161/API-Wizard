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


def to_data(self):
    'Return this DebitNote as a dictionary that can be encoded as json\n\n               Returns:\n                    dict: Dictionary to be converted to JSON\n\n        '
    data = {}
    if (not self.is_null()):
        from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
        data['transaction'] = self._transaction.to_data()
        data['account_uid'] = self._account_uid
        data['authorisation'] = self._authorisation.to_data()
        data['is_provisional'] = self._is_provisional
        data['datetime'] = _datetime_to_string(self._datetime)
        data['uid'] = self._uid
        if self._is_provisional:
            data['receipt_by'] = _datetime_to_string(self._receipt_by)
    return data
