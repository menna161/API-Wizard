from typing import Tuple
from urllib.parse import quote
from base64 import b64encode
import json
import io
import requests
import matplotlib.pyplot as plt
from qdata.errors import QdataError, ErrorCode
from .common import get_gid, get_cur_timestamp, format_callback_resp, get_shaone, get_sig
from .config import EXIN_TOKEN


def show_qrcode(url: str):
    resp = session.get(url)
    im = plt.imread(io.BytesIO(resp.content))
    plt.imshow(im)
    plt.show()
