import requests
import json
from datetime import datetime, timedelta
import pytz
from .auth import get_headers
from .parks import Park
from .pointsofinterest import PointOfInterest
from .ids import themeparkapi_ids, WDW_ID, DLR_ID
from .characters import Character


def get_possible_ids(self):
    'Returns a list of possible ids of this entityType'
    entertainments = []
    dest_data = requests.get('https://api.wdpro.disney.go.com/facility-service/destinations/{}'.format(self.__anc_dest_id), headers=get_headers()).json()
    data = requests.get(dest_data['links']['entertainments']['href'], headers=get_headers()).json()
    for enter in data['entries']:
        try:
            entertainments.append(enter['links']['self']['href'].split('/')[(- 1)].split('?')[0])
        except:
            pass
    return entertainments
