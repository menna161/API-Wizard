from json.decoder import JSONDecodeError
import time
import requests
from requests.exceptions import RequestException
from .owlet import Owlet
from .owletexceptions import OwletTemporaryCommunicationException
from .owletexceptions import OwletPermanentCommunicationException
from .owletexceptions import OwletNotInitializedException


def login(self):
    'Login to Owlet Cloud Service and obtain Auth Token.'
    login_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    login_url = (self.base_user_url + 'sign_in.json')
    login_payload = {'user': {'email': self._email, 'password': self._password, 'application': {'app_id': 'OWL-id', 'app_secret': 'OWL-4163742'}}}
    try:
        result = requests.post(login_url, json=login_payload, headers=login_headers, timeout=5)
    except RequestException:
        raise OwletTemporaryCommunicationException('Login request failed - no response')
    if (result.status_code == 401):
        raise OwletPermanentCommunicationException('Login failed, check username and password')
    if (result.status_code != 200):
        raise OwletTemporaryCommunicationException('Login request failed - status code')
    try:
        json_result = result.json()
    except JSONDecodeError:
        raise OwletTemporaryCommunicationException('Server did not send valid json')
    if (('access_token' not in json_result) or ('expires_in' not in json_result)):
        raise OwletTemporaryCommunicationException('Server did not send access token')
    self._auth_token = json_result['access_token']
    self._expiry_time = (time.time() + json_result['expires_in'])
