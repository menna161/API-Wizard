import json
from datetime import datetime, timedelta
import requests
import pytz
from .auth import get_headers
from .ids import themeparkapi_ids, WDW_ID, DLR_ID
from .characters import Character


def get_themeparkapi_data(self):
    'Returns the dictionary from the themepark api for the given id'
    park = themeparkapi_ids[self.__anc_park_id]
    themepark_id = f'{park}_{self.__id}'
    all_data = requests.get(f'https://api.themeparks.wiki/preview/parks/{park}/waittime').json()
    for i in all_data:
        if (i['id'] == themepark_id):
            return i
    return None
