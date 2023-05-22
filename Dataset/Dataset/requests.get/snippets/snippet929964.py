from typing import List, Dict, Tuple
from urllib.parse import urlencode, quote
from base64 import b64encode
import math
import datetime
import json
from Crypto.Cipher import AES
from qdata.errors import ErrorCode, QdataError
import requests


def http_get(url: str, cookies: str, cipher_text: str='') -> str:
    '\n        发送get请求, 程序中所有的get都是调这个方法\n        如果想使用多cookies抓取, 和请求重试功能\n        在这自己添加\n    '
    cur_headers = headers.copy()
    cur_headers['Cookie'] = cookies
    if cipher_text:
        cur_headers['Cipher-Text'] = cipher_text
    try:
        response = requests.get(url, headers=cur_headers, timeout=30)
    except requests.Timeout as exc:
        raise QdataError(ErrorCode.NETWORK_ERROR) from exc
    if (response.status_code != 200):
        raise QdataError(ErrorCode.NETWORK_ERROR)
    return response.text
