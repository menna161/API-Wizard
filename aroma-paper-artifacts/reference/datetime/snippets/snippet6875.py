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


def cash(self, spend, resource, receipt_within=3600):
    "Cash this cheque, specifying how much to be cashed,\n           and the resource that will be paid for\n           using this cheque. This will send the cheque to the\n           accounting service (if we trust that accounting service).\n           The accounting service will check that the cheque is valid,\n           and the signature of the item is correct. It will then\n           withdraw 'spend' funds from the account that signed the\n           cheque, returning valid CreditNote(s) that can be trusted\n           to show that the funds exist.\n\n           If 'receipt_within' is set, then the CreditNotes will\n           be automatically cancelled if they are not\n           receipted within 'receipt_within' seconds\n\n           It is your responsibility to receipt the note for\n           the actual valid incurred once the service has been\n           delivered, thereby actually transferring the cheque\n           funds into your account (on that accounting service)\n\n           This returns a list of the CreditNote(s) that were\n           cashed from the cheque\n\n           Args:\n                spend (Decimal): Value to withdraw\n                resource (str): Resource to spend value on\n                receipt_within (datetime, default=3600): Time to receipt\n                the cashing of this cheque by\n           Returns:\n                list: List of CreditNotes\n\n        "
    if (self._cheque is None):
        raise PaymentError('You cannot cash a null cheque!')
    from Acquire.Service import get_this_service as _get_this_service
    service = _get_this_service(need_private_access=True)
    self._cheque = service.sign_data(self._cheque)
    accounting_service = self.accounting_service()
    from Acquire.ObjectStore import get_datetime_future as _get_datetime_future
    receipt_by = _get_datetime_future(receipt_within)
    account_uid = service.service_user_account_uid(accounting_service=accounting_service)
    from Acquire.ObjectStore import decimal_to_string as _decimal_to_string
    from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
    from Acquire.ObjectStore import string_to_list as _string_to_list
    result = accounting_service.call_function(function='cash_cheque', args={'cheque': self.to_data(), 'spend': _decimal_to_string(spend), 'resource': str(resource), 'account_uid': account_uid, 'receipt_by': _datetime_to_string(receipt_by)})
    credit_notes = None
    try:
        from Acquire.Accounting import CreditNote as _CreditNote
        credit_notes = _string_to_list(result['credit_notes'], _CreditNote)
    except Exception as e:
        raise PaymentError(('Attempt to cash the cheque has not resulted in a valid CreditNote? Error = %s' % str(e)))
    total_cashed = 0
    for note in credit_notes:
        total_cashed = (total_cashed + note.value())
        if (note.account_uid() != account_uid):
            raise PaymentError(('The cashed cheque is paying into the wrong account! %s. It should be going to %s' % (note.account_uid(), account_uid)))
    if (total_cashed != spend):
        raise PaymentError(('The value of the cheque (%s) does not match the total value of the credit note(s) returned (%s)' % (spend, total_cashed)))
    return credit_notes
