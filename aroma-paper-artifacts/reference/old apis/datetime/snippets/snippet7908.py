from enum import Enum as _Enum
from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
from Acquire.Accounting import create_decimal as _create_decimal
from Acquire.ObjectStore import datetime_to_string as _datetime_to_string
import copy as _copy
from Acquire.Accounting import create_decimal as _create_decimal


@staticmethod
def from_key(key):
    "Extract information from the passed object store key.\n\n           This looks for a string that is;\n\n           isoformat_datetime/UID/transactioncode\n\n           where transactioncode is a string that matches\n           '2 letters followed by a number'\n\n           CL000100.005000\n           DR000004.234100\n\n           etc.\n\n           For sent and received receipts there are two values;\n           the receipted value and the original estimate. These\n           have the standard format if the values are the same, e.g.\n\n           RR000100.005000\n\n           however, they have original value T receipted value if they are\n           different, e.g.\n\n           RR000100.005000T000090.000000\n\n           Args:\n                key: Object store key\n\n        "
    from Acquire.ObjectStore import string_to_datetime as _string_to_datetime
    from Acquire.Accounting import create_decimal as _create_decimal
    parts = key.split('/')
    nparts = len(parts)
    for i in range(0, nparts):
        j = ((nparts - i) - 1)
        t = TransactionInfo()
        try:
            t._datetime = _string_to_datetime(parts[(j - 2)])
        except:
            continue
        t._uid = parts[(j - 1)]
        part = parts[j]
        try:
            code = TransactionInfo._get_code(part[0:2])
            if ((code == TransactionCode.SENT_RECEIPT) or (code == TransactionCode.RECEIVED_RECEIPT)):
                values = part[2:].split('T')
                try:
                    value = _create_decimal(values[0])
                    receipted_value = _create_decimal(values[1])
                    t._code = code
                    t._value = value
                    t._receipted_value = receipted_value
                    return t
                except:
                    pass
            value = _create_decimal(part[2:])
            t._code = code
            t._value = value
            t._receipted_value = None
            return t
        except:
            pass
    raise ValueError(("Cannot extract transaction info from '%s'" % key))
