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


def _refresh(self, force_update=False):
    'Refresh the current status of this account. This fetches\n           the latest data, e.g. balance, limits etc. Note that this\n           limits you to refreshing at most once every five seconds...\n\n           Args:\n                force_update (bool, default=False): Force the refresh\n           Returns:\n                None\n        '
    if self.is_null():
        from Acquire.Accounting import create_decimal as _create_decimal
        from Acquire.Accounting import Balance as _Balance
        self._overdraft_limit = _create_decimal(0)
        self._balance = _Balance()
        return
    if force_update:
        should_refresh = True
    else:
        should_refresh = False
        if (self._last_update is None):
            should_refresh = True
        else:
            should_refresh = ((_datetime.datetime.now() - self._last_update).seconds > 5)
    if (not should_refresh):
        return
    if (not self.is_logged_in()):
        raise PermissionError('You cannot get information about this account until after the owner has successfully authenticated.')
    from Acquire.Client import Authorisation as _Authorisation
    from Acquire.Accounting import create_decimal as _create_decimal
    service = self.accounting_service()
    auth = _Authorisation(resource=('get_info %s' % self._account_uid), user=self._user)
    args = {'authorisation': auth.to_data(), 'account_name': self.name(), 'account_uid': self.uid()}
    result = service.call_function(function='get_info', args=args)
    from Acquire.Accounting import Balance as _Balance
    self._balance = _Balance.from_data(result['balance'])
    self._overdraft_limit = _create_decimal(result['overdraft_limit'])
    self._description = result['description']
    self._last_update = _datetime.datetime.now()
