import argparse
import codecs
import datetime
import json
import os
import sys
import time
import subprocess
from xml.dom.minidom import parseString
from instagram_private_api import ClientError
from instagram_private_api import Client
import urllib.request as urllib
from instagram_private_api import Client, ClientError, ClientLoginError, ClientCookieExpiredError, ClientLoginRequiredError, __version__ as client_version
import urllib as urllib
import sys
from instagram_private_api import Client, ClientError, ClientLoginError, ClientCookieExpiredError, ClientLoginRequiredError, __version__ as client_version


def login(username='', password=''):
    device_id = None
    try:
        settings_file = 'credentials.json'
        if (not os.path.isfile(settings_file)):
            print('[W] Unable to find auth cookie file: {0!s} (creating a new one...)'.format(settings_file))
            api = Client(username, password, on_login=(lambda x: onlogin_callback(x, settings_file)))
        else:
            with open(settings_file) as file_data:
                cached_settings = json.load(file_data, object_hook=from_json)
            device_id = cached_settings.get('device_id')
            api = Client(username, password, settings=cached_settings)
            print((('[I] Using cached login cookie for "' + api.authenticated_user_name) + '".'))
    except (ClientCookieExpiredError, ClientLoginRequiredError) as e:
        print('[E] ClientCookieExpiredError/ClientLoginRequiredError: {0!s}'.format(e))
        if (username and password):
            api = Client(username, password, device_id=device_id, on_login=(lambda x: onlogin_callback(x, settings_file)))
        else:
            print('[E] The login cookie has expired, but no login arguments were given.')
            print('[E] Please supply --username and --password arguments.')
            print(('-' * 70))
            sys.exit(0)
    except ClientLoginError as e:
        print('[E] Could not login: {:s}.\n[E] {:s}\n\n{:s}'.format(json.loads(e.error_response).get('error_title', 'Error title not available.'), json.loads(e.error_response).get('message', 'Not available'), e.error_response))
        print(('-' * 70))
        sys.exit(9)
    except ClientError as e:
        print('[E] Client Error: {:s}'.format(e.error_response))
        print(('-' * 70))
        sys.exit(9)
    except Exception as e:
        if str(e).startswith('unsupported pickle protocol'):
            print('[W] This cookie file is not compatible with Python {}.'.format(sys.version.split(' ')[0][0]))
            print("[W] Please delete your cookie file 'credentials.json' and try again.")
        else:
            print('[E] Unexpected Exception: {0!s}'.format(e))
        print(('-' * 70))
        sys.exit(99)
    print((('[I] Login to "' + api.authenticated_user_name) + '" OK!'))
    cookie_expiry = api.cookie_jar.auth_expires
    print('[I] Login cookie expiry date: {0!s}'.format(datetime.datetime.fromtimestamp(cookie_expiry).strftime('%Y-%m-%d at %I:%M:%S %p')))
    return api
