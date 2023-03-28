import base64
import math
import datetime
from collections import OrderedDict
from OpenSSL import crypto
from construct import Struct, Byte, Int16ub, Int64ub, Enum, Bytes, Int24ub, this, GreedyBytes, GreedyRange, Terminated, Embedded


def dump_cert(certificate):
    subject = certificate.get_subject()
    try:
        not_before = datetime.datetime.strptime(certificate.get_notBefore().decode('ascii'), '%Y%m%d%H%M%SZ').timestamp()
    except:
        not_before = 0
    try:
        not_after = datetime.datetime.strptime(certificate.get_notAfter().decode('ascii'), '%Y%m%d%H%M%SZ').timestamp()
    except:
        not_after = 0
    return {'subject': {'aggregated': repr(certificate.get_subject())[18:(- 2)], 'C': subject.C, 'ST': subject.ST, 'L': subject.L, 'O': subject.O, 'OU': subject.OU, 'CN': subject.CN}, 'extensions': dump_extensions(certificate), 'not_before': not_before, 'not_after': not_after, 'as_der': base64.b64encode(crypto.dump_certificate(crypto.FILETYPE_ASN1, certificate)).decode('utf-8')}
