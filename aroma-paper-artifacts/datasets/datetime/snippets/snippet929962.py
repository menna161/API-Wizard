from typing import List, Dict, Tuple
from urllib.parse import urlencode, quote
from base64 import b64encode
import math
import datetime
import json
from Crypto.Cipher import AES
from qdata.errors import ErrorCode, QdataError
import requests


def get_cipher_text(keyword: str) -> str:
    byte_list = [b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08', b'\t', b'\n', b'\x0b', b'\x0c', b'\r', b'\x0e', b'\x0f', b'\x10']
    start_time = 1652338834776
    end_time = int((datetime.datetime.now().timestamp() * 1000))
    wait_encrypted_data = {'ua': headers['User-Agent'], 'url': quote(f'https://index.baidu.com/v2/main/index.html#/trend/{keyword}?words={keyword}'), 'platform': 'MacIntel', 'clientTs': end_time, 'version': '2.1.0'}
    password = b'yyqmyasygcwaiyaa'
    iv = b'1234567887654321'
    aes = AES.new(password, AES.MODE_CBC, iv)
    wait_encrypted_str = json.dumps(wait_encrypted_data).encode()
    filled_count = (16 - (len(wait_encrypted_str) % 16))
    wait_encrypted_str += (byte_list[filled_count] * filled_count)
    encrypted_str = aes.encrypt(wait_encrypted_str)
    cipher_text = f'{start_time}_{end_time}_{b64encode(encrypted_str).decode()}'
    return cipher_text
