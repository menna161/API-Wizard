import json
import requests
import sys, cgi, os, gzip
from StringIO import BytesIO
from io import BytesIO


def authenticate(self):
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    url = 'https://account-api.icann.org/api/authenticate'
    response = requests.post(url, data=json.dumps(self.credential), headers=headers)
    status_code = response.status_code
    if (status_code == 200):
        access_token = response.json()['accessToken']
        return access_token
    elif (status_code == 404):
        sys.stderr.write(('Invalid url ' + url))
        exit(1)
    elif (status_code == 401):
        sys.stderr.write('Invalid username/password. Please reset your password via web')
        exit(1)
    elif (status_code == 500):
        sys.stderr.write('Internal server error. Please try again later')
        exit(1)
    else:
        sys.stderr.write('Failed to authenticate with error code {1}'.format(status_code))
        exit(1)
