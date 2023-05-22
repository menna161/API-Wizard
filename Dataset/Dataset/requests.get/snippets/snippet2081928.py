import requests
from datetime import datetime, timedelta
import pytz
from .auth import get_headers
from .parks import Park
from .entertainments import Entertainment
from .attractions import Attraction
from .ids import WDW_PARK_IDS, DLR_PARK_IDS, WDW_ID, DLR_ID, DESTINATION_IDS, themeparkapi_ids


def get_themeparkapi_data(self):
    'Returns the list of dictionaries for all parks from the themeparks api'
    all_data = []
    if (self.__id == WDW_ID):
        parks = WDW_PARK_IDS
    else:
        parks = DLR_PARK_IDS
    for id in parks:
        try:
            park = themeparkapi_ids[id]
            all_data.extend(requests.get(f'https://api.themeparks.wiki/preview/parks/{park}/waittime').json())
        except:
            continue
    return all_data
