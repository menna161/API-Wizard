from .auth import get_headers
import requests
import json


def ids(dest, type):
    dest_data = requests.get('https://api.wdpro.disney.go.com/facility-service/destinations/{}'.format(dest), headers=get_headers()).json()
    ids = []
    data = requests.get(dest_data['links'][type]['href'], headers=get_headers()).json()
    for enter in data['entries']:
        try:
            ids.append(enter['links']['self']['href'].split('/')[(- 1)].split('?')[0])
        except:
            pass
    return ids
