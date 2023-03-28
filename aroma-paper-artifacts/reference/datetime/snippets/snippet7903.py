from enum import Enum as _Enum
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
import copy as _copy
from Acquire.Accounting import create_decimal as _create_decimal


def rescind(self):
    "Return a TransactionInfo that corresponds to rescinding this\n           transaction info. This is useful if you want to update the\n           ledger to remove this object (since we can't delete anything\n           from the ledger)\n        "
    t = TransactionInfo()
    t._uid = self._uid[(- 1)::(- 1)]
    t._value = self._value
    t._datetime = self._datetime
    if (self._code is TransactionCode.DEBIT):
        t._code = TransactionCode.CREDIT
    elif (self._code is TransactionCode.CREDIT):
        t._code = TransactionCode.DEBIT
    elif (self._code is TransactionCode.CURRENT_LIABILITY):
        t._value = (- self._value)
    elif (self._code is TransactionCode.ACCOUNT_RECEIVABLE):
        t._value = (- self._value)
    else:
        raise PermissionError(('Do not have permission to rescind a %s' % str(self)))
    return t
