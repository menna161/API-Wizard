from datetime import timedelta
import arrow
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
import requests


def _refresh_tokens(self, client_id, client_secret):
    '\n        Refresh access token.\n        '
    response = requests.post('https://www.openhumans.org/oauth2/token/', data={'grant_type': 'refresh_token', 'refresh_token': self.refresh_token}, auth=requests.auth.HTTPBasicAuth(client_id, client_secret))
    if (response.status_code == 200):
        data = response.json()
        self.access_token = data['access_token']
        self.refresh_token = data['refresh_token']
        self.token_expires = self.get_expiration(data['expires_in'])
        self.save()
