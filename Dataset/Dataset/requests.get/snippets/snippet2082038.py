import requests
import json
import pytz
from datetime import datetime, timedelta
from .auth import get_headers
from .ids import themeparkapi_ids, WDW_ID, DLR_ID


def get_themeparkapi_data(self):
    'Returns the list of dictionaries from the themepark api for the given id'
    park = themeparkapi_ids[self.__anc_park_id]
    all_data = requests.get(f'https://api.themeparks.wiki/preview/parks/{park}/waittime').json()
    return all_data
