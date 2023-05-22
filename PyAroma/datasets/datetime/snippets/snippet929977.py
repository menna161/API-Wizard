from datetime import datetime
from base64 import b64encode
from typing import Dict
import re
import uuid
import hashlib
from Crypto.Cipher import AES


def get_cur_timestamp() -> int:
    return int((datetime.now().timestamp() * 1000))
