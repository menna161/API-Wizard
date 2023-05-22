import logging
from rsa._compat import b
import rsa.prime
import rsa.pem
import rsa.common
import rsa.randnum
import rsa.core
import doctest
from pyasn1.codec.der import decoder
from rsa.asn1 import AsnPubKey
from pyasn1.codec.der import encoder
from rsa.asn1 import AsnPubKey
from rsa.asn1 import OpenSSLPubKey
from pyasn1.codec.der import decoder
from pyasn1.type import univ
from pyasn1.codec.der import decoder
from pyasn1.type import univ, namedtype
from pyasn1.codec.der import encoder
from rsa import parallel
import functools


def blinded_decrypt(self, encrypted):
    'Decrypts the message using blinding to prevent side-channel attacks.\n\n        :param encrypted: the encrypted message\n        :type encrypted: int\n\n        :returns: the decrypted message\n        :rtype: int\n        '
    blind_r = rsa.randnum.randint((self.n - 1))
    blinded = self.blind(encrypted, blind_r)
    decrypted = rsa.core.decrypt_int(blinded, self.d, self.n)
    return self.unblind(decrypted, blind_r)
