from datetime import datetime
from base64 import b64encode
from typing import Dict
import re
import uuid
import hashlib
from Crypto.Cipher import AES


def get_shaone() -> str:
    cur_timestamp = str(int((datetime.now().timestamp() * 1000)))
    m5 = hashlib.md5(cur_timestamp.encode()).hexdigest()
    return hashlib.sha1(m5.encode()).hexdigest()
