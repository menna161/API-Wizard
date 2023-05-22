import requests
from datetime import datetime, timedelta
import pytz
from .auth import get_headers
from .parks import Park
from .entertainments import Entertainment
from .attractions import Attraction
from .ids import WDW_PARK_IDS, DLR_PARK_IDS, WDW_ID, DLR_ID, DESTINATION_IDS, themeparkapi_ids


def get_entertainment_ids(self):
    '\n        Returns a list of Entertainment IDs\n        '
    entertainments = []
    data = requests.get(self.__data['links']['entertainments']['href'], headers=get_headers()).json()
    for enter in data['entries']:
        try:
            entertainments.append(enter['links']['self']['href'].split('/')[(- 1)].split('?')[0])
        except:
            pass
    return entertainments
