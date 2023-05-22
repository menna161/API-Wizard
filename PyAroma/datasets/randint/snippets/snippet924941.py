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


def see_reels(self, reels):
    '\n            Input - the list of reels jsons\n            They can be aquired by using get_users_reel()\n            or get_user_reel() methods\n        '
    if (not isinstance(reels, list)):
        reels = [reels]
    story_seen = {}
    now = int(time.time())
    for (i, story) in enumerate(sorted(reels, key=(lambda m: m['taken_at']), reverse=True)):
        story_seen_at = (now - min(((i + 1) + random.randint(0, 2)), max(0, (now - story['taken_at']))))
        story_seen['{!s}_{!s}'.format(story['id'], story['user']['pk'])] = ['{!s}_{!s}'.format(story['taken_at'], story_seen_at)]
    data = self.json_data({'reels': story_seen, '_csrftoken': self.token, '_uuid': self.uuid, '_uid': self.user_id})
    data = self.generate_signature(data)
    return self.session.post(('https://i.instagram.com/api/v2/' + 'media/seen/'), data=data).ok
