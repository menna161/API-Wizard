import requests
import json
import pytz
from datetime import datetime, timedelta
from .auth import get_headers
from .ids import themeparkapi_ids, WDW_ID, DLR_ID


def get_entertainment_ids(self):
    'Returns a list of entertainments for this object'
    ids = []
    data = requests.get('https://api.wdpro.disney.go.com/facility-service/{}s/{}/entertainments?region=us'.format(self.__entityType, self.__id), headers=get_headers()).json()
    for entry in data['entries']:
        try:
            ids.append(entry['links']['self']['href'].split('/')[(- 1)].split('?')[0])
        except:
            pass
    return ids
