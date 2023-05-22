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


def get_timeline_feed(self, reason=None, options=[]):
    headers = {'X-Ads-Opt-Out': '0'}
    data = {'feed_view_info': '[]', 'phone_id': self.phone_id, 'battery_level': random.randint(25, 100), 'timezone_offset': '0', '_csrftoken': self.token, 'device_id': self.uuid, 'request_id': self.uuid, '_uuid': self.uuid, 'is_charging': random.randint(0, 1), 'will_sound_on': random.randint(0, 1), 'session_id': self.client_session_id, 'bloks_versioning_id': 'e538d4591f238824118bfcb9528c8d005f2ea3becd947a3973c030ac971bb88e'}
    if ('is_pull_to_refresh' in options):
        data['reason'] = 'pull_to_refresh'
        data['is_pull_to_refresh'] = '1'
    elif ('is_pull_to_refresh' not in options):
        data['reason'] = 'cold_start_fetch'
        data['is_pull_to_refresh'] = '0'
    if ('push_disabled' in options):
        data['push_disabled'] = 'true'
    if ('recovered_from_crash' in options):
        data['recovered_from_crash'] = '1'
    data = json.dumps(data)
    return self.send_request('feed/timeline/', data, with_signature=False, headers=headers)
