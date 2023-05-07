import base64
import datetime
import hashlib
import hmac
import json
import logging
import os
import random
import sys
import time
import uuid
import secrets
import pytz
import requests
import requests.utils
import six.moves.urllib as urllib
from requests_toolbelt import MultipartEncoder
from tqdm import tqdm
from Crypto.PublicKey import RSA
import rsa
from Cryptodome.Cipher import AES
from . import config, devices
from .api_login import change_device_simulation, generate_all_uuids, load_uuid_and_cookie, login_flow, pre_login_flow, reinstall_app_simulation, save_uuid_and_cookie, set_device, sync_launcher, get_prefill_candidates, get_account_family, get_zr_token_result, banyan, igtv_browse_feed, sync_device_features, creatives_ar_class, set_contact_point_prefill
from .api_photo import configure_photo, download_photo, upload_photo, upload_album
from .api_story import configure_story, download_story, upload_story_photo
from .api_video import configure_video, download_video, upload_video
from .prepare import delete_credentials, get_credentials
from json.decoder import JSONDecodeError
from io import StringIO


def gen_user_breadcrumb(self, size):
    key = 'iN4$aGr0m'
    dt = int((time.time() * 1000))
    time_elapsed = (random.randint(500, 1500) + (size * random.randint(500, 1500)))
    text_change_event_count = max(1, (size / random.randint(3, 5)))
    data = '{size!s} {elapsed!s} {count!s} {dt!s}'.format(**{'size': size, 'elapsed': time_elapsed, 'count': text_change_event_count, 'dt': dt})
    return '{!s}\n{!s}\n'.format(base64.b64encode(hmac.new(key.encode('ascii'), data.encode('ascii'), digestmod=hashlib.sha256).digest()), base64.b64encode(data.encode('ascii')))
