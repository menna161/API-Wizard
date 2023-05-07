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


def like(self, media_id, double_tap=None, container_module='feed_short_url', feed_position=0, username=None, user_id=None, hashtag_name=None, hashtag_id=None, entity_page_name=None, entity_page_id=None):
    data = self.action_data({'inventory_source': 'media_or_ad', 'media_id': media_id, '_csrftoken': self.token, 'radio_type': 'wifi-none', '_uid': self.user_id, '_uuid': self.uuid, 'is_carousel_bumped_post': 'false', 'container_module': container_module, 'feed_position': str(feed_position)})
    if (container_module == 'feed_timeline'):
        data.update({'inventory_source': 'media_or_ad'})
    if username:
        data.update({'username': username, 'user_id': user_id})
    if hashtag_name:
        data.update({'hashtag_name': hashtag_name, 'hashtag_id': hashtag_id})
    if entity_page_name:
        data.update({'entity_page_name': entity_page_name, 'entity_page_id': entity_page_id})
    double_tap = random.randint(0, 1)
    json_data = self.json_data(data)
    self.logger.debug('post data: {}'.format(json_data))
    return self.send_request(endpoint='media/{media_id}/like/'.format(media_id=media_id), post=json_data, extra_sig=['d={}'.format(double_tap)])
