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


def read(self, spend, resource, receipt_by):
    'Read the cheque - this will read the cheque to return the\n           decrypted contents. This will only work if this function\n           is called on the accounting service that will cash the\n           cheque, if the signature on the cheque matches the\n           service that is authorised to cash the cheque, and\n           if the passed resource matches the resource\n           encoded in the cheque. If this is all correct, then the\n           returned dictionary will contain;\n\n           {"recipient_url": The URL of the service which was sent the cheque,\n            "recipient_key_fingerprint": Verified fingerprint of the service\n                                         key that signed this cheque\n            "spend": The amount authorised by this cheque,\n            "uid": The unique ID for this cheque,\n            "resource": String that identifies the resource this cheque will\n                        be used to pay for,\n            "account_uid": UID of the account from which funds will be drawn\n            "authorisation" : Verified authorisation from the user who\n                              says they own the account for the spend\n            "receipt_by" : Time when we must receipt the cheque, or\n                           we will lose the money\n           }\n\n           You must pass in the spend you want to draw from the cheque,\n           a string representing the resource this cheque will\n           be used to pay for, and the time by which you promise to receipt\n           the cheque after cashing\n\n           Args:\n                spend (Decimal): Amount authorised by cheque\n                resource (str): Resource to pay for\n                receipt_by (datetime): Time cheque must be receipted\n                by\n           Returns:\n                dict: Dictionary described above\n\n        '
    if (self._cheque is None):
        raise PaymentError('You cannot read a null cheque')
    from Acquire.ObjectStore import string_to_decimal as _string_to_decimal
    from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
    from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
    from Acquire.Service import get_this_service as _get_this_service
    spend = _string_to_decimal(spend)
    resource = str(resource)
    receipt_by = _string_to_datetime(receipt_by)
    service = _get_this_service(need_private_access=True)
    try:
        cheque_data = _json.loads(self._cheque['signed_data'])
    except:
        cheque_data = self._cheque
    cheque_data = service.decrypt_data(cheque_data)
    from Acquire.Identity import Authorisation as _Authorisation
    auth = _Authorisation.from_data(cheque_data['authorisation'])
    info = cheque_data['info']
    auth_resource = info
    try:
        auth.verify(resource=info)
    except Exception as e:
        raise PaymentError(("The user's signature/authorisation for this cheque is not valid! ERROR: %s" % str(e)))
    info = _json.loads(info)
    info['authorisation'] = auth
    try:
        recipient_url = info['recipient_url']
    except:
        recipient_url = None
    if recipient_url:
        recipient_service = service.get_trusted_service(service_url=recipient_url)
        recipient_service.verify_data(self._cheque)
        info['recipient_key_fingerprint'] = self._cheque['fingerprint']
    try:
        cheque_resource = info['resource']
    except:
        cheque_resource = None
    if (cheque_resource is not None):
        if (resource != resource):
            raise PaymentError('Disagreement over the resource for which this cheque has been signed')
    info['resource'] = resource
    info['auth_resource'] = auth_resource
    try:
        max_spend = info['max_spend']
        del info['max_spend']
    except:
        max_spend = None
    if (max_spend is not None):
        max_spend = _string_to_decimal(max_spend)
        if (max_spend < spend):
            raise PaymentError(('The requested spend (%s) exceeds the authorised maximum value of the cheque' % spend))
    info['spend'] = spend
    try:
        expiry_date = info['expiry_date']
        del expiry_date['expiry_date']
    except:
        expiry_date = None
    if (expiry_date is not None):
        expiry_date = _string_to_datetime(expiry_date)
        from Acquire.ObjectStore import get_datetime_now as _get_datetime_now
        now = _get_datetime_now()
        if (now > receipt_by):
            raise PaymentError('The time when you promised to receipt the cheque has already passed!')
        if (receipt_by > expiry_date):
            raise PaymentError(('The cheque will have expired after you plan to receipt it!: %s versus %s' % (_datetime_to_string(receipt_by), _datetime_to_string(expiry_date))))
    info['receipt_by'] = receipt_by
    return info
