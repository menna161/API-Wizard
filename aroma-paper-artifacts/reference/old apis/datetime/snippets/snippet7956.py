import uuid as _uuid
import datetime as _datetime
from copy import copy as _copy
from enum import Enum as _Enum
from ._errors import TransactionError, UnbalancedLedgerError, UnmatchedReceiptError, UnmatchedRefundError, LedgerError
from Acquire.Accounting import Ledger as _Ledger
from Acquire.Accounting import Ledger as _Ledger
from Acquire.Accounting import Ledger as _Ledger
from Acquire.ObjectStore import Mutex as _Mutex
from Acquire.Accounting import Transaction as _Transaction
from Acquire.Service import get_service_account_bucket as _get_service_account_bucket
from Acquire.Accounting import CreditNote as _CreditNote
from Acquire.Accounting import DebitNote as _DebitNote
from Acquire.Accounting import Refund as _Refund
from Acquire.Accounting import Receipt as _Receipt


def datetime(self):
    'Return the datetime when this transaction was applied\n\n           Returns:\n                datetime: Datetime at which transaction was applied\n        '
    if self.is_null():
        return None
    else:
        return self.debit_note().datetime()
