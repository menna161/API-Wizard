import datetime as _datetime
import json as _json
from ._errors import PaymentError
from Acquire.Client import Account as _Account
from Acquire.ObjectStore import create_uid as _create_uid
from Acquire.Identity import Authorisation as _Authorisation
from Acquire.ObjectStore import string_to_decimal as _string_to_decimal
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Service import get_this_service as _get_this_service
from Acquire.Identity import Authorisation as _Authorisation
from Acquire.Service import get_this_service as _get_this_service
from Acquire.ObjectStore import get_datetime_future as _get_datetime_future
from Acquire.ObjectStore import decimal_to_string as _decimal_to_string
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.ObjectStore import string_to_list as _string_to_list
from Acquire.Service import get_this_service as _get_this_service
from Acquire.ObjectStore import decimal_to_string as _decimal_to_string
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
from Acquire.Service import Service as _Service
from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
from Acquire.Accounting import CreditNote as _CreditNote
from Acquire.Service import ServiceError
from Acquire.Service import Service as _Service


@staticmethod
def write(account=None, resource=None, recipient=None, recipient_url=None, max_spend=None, expiry_date=None):
    "Create and return a cheque that can be used at any point\n           in the future to authorise a transaction. If 'recipient_url'\n           is supplied, then only the service with the matching\n           URL can 'cash' the cheque (it will need to sign the cheque\n           before sending it to the accounting service). If 'max_spend'\n           is specified, then the cheque is only valid up to that\n           maximum spend. Otherwise, it is valid up to the maximum\n           daily spend limit (or other limits) of the account. If\n           'expiry_date' is supplied then this cheque is valid only\n           before the supplied datetime. If 'resource' is\n           supplied then this cheque is only valid to pay for the\n           specified resource (this should be a string that everyone\n           agrees represents the resource in question). Note that\n           this cheque is for a future transaction. We do not check\n           to see if there are sufficient funds now, and this does\n           not affect the account. If there are insufficient funds\n           when the cheque is cashed (or it breaks spending limits)\n           then the cheque will bounce.\n        "
    from Acquire.Client import Account as _Account
    if (not isinstance(account, _Account)):
        raise TypeError('You must pass a valid Acquire.Client.Account object to write a cheque...')
    if (max_spend is not None):
        from Acquire.ObjectStore import decimal_to_string as _decimal_to_string
        max_spend = _decimal_to_string(max_spend)
    if (expiry_date is not None):
        from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
        expiry_date = _datetime_to_string(expiry_date)
    if (recipient is not None):
        from Acquire.Service import Service as _Service
        recipient_url = _Service.resolve(recipient)['service_url']
    elif (recipient_url is not None):
        from Acquire.Service import Service as _Service
        recipient_url = _Service.resolve(recipient_url)['service_url']
    else:
        raise PermissionError('You have to specify the recipient of the cheque!')
    from Acquire.ObjectStore import create_uid as _create_uid
    from Acquire.Identity import Authorisation as _Authorisation
    cheque_uid = _create_uid(include_date=True, short_uid=True)
    info = _json.dumps({'recipient_url': recipient_url, 'max_spend': max_spend, 'expiry_date': expiry_date, 'uid': cheque_uid, 'resource': str(resource), 'account_uid': account.uid()})
    auth = _Authorisation(user=account.user(), resource=info)
    data = {'info': info, 'authorisation': auth.to_data()}
    cheque = Cheque()
    cheque._cheque = account.accounting_service().encrypt_data(data)
    cheque._accounting_service_url = account.accounting_service().canonical_url()
    return cheque
