import requests
from datetime import datetime, timedelta
import pytz
from .auth import get_headers
from .parks import Park
from .entertainments import Entertainment
from .attractions import Attraction
from .ids import WDW_PARK_IDS, DLR_PARK_IDS, WDW_ID, DLR_ID, DESTINATION_IDS, themeparkapi_ids


def get_attraction_ids(self):
    '\n        Returns a list of Attraction IDs\n        '
    attractions = []
    data = requests.get(self.__data['links']['attractions']['href'], headers=get_headers()).json()
    for attract in data['entries']:
        try:
            attractions.append(attract['links']['self']['href'].split('/')[(- 1)].split('?')[0])
        except:
            pass
    return attractions
