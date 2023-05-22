import os
from . import missing_app_tokens, missing_widget_tokens
import requests
from requests_oauthlib import OAuth1
from mkmsdk.MKMOAuth1 import MKMOAuth1
from mkmsdk.MKMClient import MKMClient


@missing_app_tokens
def test_widget_app_oauth1_is_correct():
    'Verifies if response from backend is positive using custom Client.'
    url = 'https://sandbox.cardmarket.com/ws/v1.1/output.json/games'
    auth = MKMOAuth1(os.environ.get('MKM_APP_TOKEN'), client_secret=os.environ.get('MKM_APP_SECRET'), resource_owner_key=os.environ.get('MKM_ACCESS_TOKEN'), resource_owner_secret=os.environ.get('MKM_ACCESS_TOKEN_SECRET'), realm=url, client_class=MKMClient)
    r = requests.get(url, auth=auth)
    assert (r.status_code == 200)
