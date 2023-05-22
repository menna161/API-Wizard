import requests
from datetime import datetime, timedelta
import pytz
from .auth import get_headers
from .parks import Park
from .entertainments import Entertainment
from .attractions import Attraction
from .ids import WDW_PARK_IDS, DLR_PARK_IDS, WDW_ID, DLR_ID, DESTINATION_IDS, themeparkapi_ids


def get_park_ids(self):
    '\n        Returns a list of theme or water park IDs\n        '
    ids = []
    data = requests.get(self.__data['links']['themeParks']['href'], headers=get_headers()).json()
    for entry in data['entries']:
        try:
            ids.append(entry['links']['self']['href'].split('/')[(- 1)].split('?')[0])
        except:
            pass
    data = requests.get(self.__data['links']['waterParks']['href'], headers=get_headers()).json()
    try:
        if (data['errors'] is not None):
            return ids
    except:
        pass
    for entry in data['entries']:
        try:
            ids.append(entry['links']['self']['href'].split('/')[(- 1)].split('?')[0])
        except:
            pass
    return ids
