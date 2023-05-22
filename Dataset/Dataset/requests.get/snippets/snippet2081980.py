import requests
import json
import pytz
from datetime import datetime, timedelta
from .auth import get_headers
from .ids import WDW_ID, DLR_ID


def get_possible_ids(self):
    'Returns a list of possible ids of this entityType'
    ids = []
    dest_data = requests.get('https://api.wdpro.disney.go.com/facility-service/destinations/{}'.format(self.__anc_dest_id), headers=get_headers()).json()
    data = requests.get(dest_data['links']['entertainmentVenues']['href'], headers=get_headers()).json()
    for entry in data['entries']:
        try:
            ids.append(entry['links']['self']['href'].split('/')[(- 1)].split('?')[0])
        except:
            pass
    return ids
