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


def login(self, username=None, password=None, force=False, proxy=None, use_cookie=True, use_uuid=True, cookie_fname=None, ask_for_code=False, set_device=True, generate_all_uuids=True, is_threaded=False):
    if (password is None):
        (username, password) = get_credentials(base_path=self.base_path, username=username)
    set_device = generate_all_uuids = True
    self.set_user(username, password)
    self.session = requests.Session()
    self.proxy = proxy
    self.set_proxy()
    self.cookie_fname = cookie_fname
    if (self.cookie_fname is None):
        fmt = '{username}_uuid_and_cookie.json'
        cookie_fname = fmt.format(username=username)
        self.cookie_fname = os.path.join(self.base_path, cookie_fname)
    cookie_is_loaded = False
    msg = 'Login flow failed, the cookie is broken. Relogin again.'
    if (use_cookie is True):
        if (self.load_uuid_and_cookie(load_cookie=use_cookie, load_uuid=use_uuid) is True):
            if (self.login_flow(False) is True):
                cookie_is_loaded = True
                self.save_successful_login()
            else:
                self.logger.info(msg)
                set_device = generate_all_uuids = False
                force = True
    if ((not cookie_is_loaded) and ((not self.is_logged_in) or force)):
        self.session = requests.Session()
        if (use_uuid is True):
            if (self.load_uuid_and_cookie(load_cookie=use_cookie, load_uuid=use_uuid) is False):
                if (set_device is True):
                    self.set_device()
                if (generate_all_uuids is True):
                    self.generate_all_uuids()
        self.pre_login_flow()
        data = json.dumps({'jazoest': str(random.randint(22000, 22999)), 'country_codes': '[{"country_code":"1","source":["default"]}]', 'phone_id': self.phone_id, '_csrftoken': self.token, 'username': self.username, 'adid': '', 'guid': self.uuid, 'device_id': self.device_id, 'google_tokens': '[]', 'password': self.password, 'login_attempt_count': '1'})
        if self.send_request('accounts/login/', data, True):
            self.save_successful_login()
            self.login_flow(True)
            return True
        elif (self.last_json.get('error_type', '') == 'checkpoint_challenge_required'):
            if (ask_for_code is True):
                solved = self.solve_challenge()
                if solved:
                    self.save_successful_login()
                    self.login_flow(True)
                    return True
                else:
                    self.logger.error('Failed to login, unable to solve the challenge')
                    self.save_failed_login()
                    return False
            else:
                return False
        elif self.last_json.get('two_factor_required'):
            if self.two_factor_auth():
                self.save_successful_login()
                self.login_flow(True)
                return True
            else:
                self.logger.error('Failed to login with 2FA!')
                self.save_failed_login()
                return False
        else:
            self.logger.error('Failed to login go to instagram and change your password')
            self.save_failed_login()
            delete_credentials(self.base_path)
            return False
