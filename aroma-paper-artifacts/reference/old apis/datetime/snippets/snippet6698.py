import datetime as _datetime
import json as _json
from Acquire.Client import Service as _Service
from Acquire.Client import AccountError
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Accounting import Transaction as _Transaction
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Client import LoginError
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.Accounting import Balance as _Balance
from Acquire.Accounting import Transaction as _Transaction
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.Client import Authorisation as _Authorisation
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.Client import Cheque as _Cheque
from Acquire.Accounting import AccountingService as _AccountingService
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.Accounting import Balance as _Balance
from Acquire.Service import Service as _Service


def last_update_time(self):
    'Return the time of the last update of the balance\n\n           Returns:\n                datetime: Datetime of last update of the account\n                balance\n        '
    return self._last_update
