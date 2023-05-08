import hashlib
import random
import struct
from enum import IntEnum
from typing import Any, Dict, Optional, Tuple, Union, cast
from ._utils import logger_warning
from .errors import DependencyError
from .generic import ArrayObject, ByteStringObject, DictionaryObject, PdfObject, StreamObject, TextStringObject, create_string_object
from Crypto.Cipher import AES, ARC4
from Crypto.Util.Padding import pad


def encrypt(self, data: bytes) -> bytes:
    iv = bytes(bytearray((random.randint(0, 255) for _ in range(16))))
    p = (16 - (len(data) % 16))
    data += bytes(bytearray((p for _ in range(p))))
    aes = AES.new(self.key, AES.MODE_CBC, iv)
    return (iv + aes.encrypt(data))
