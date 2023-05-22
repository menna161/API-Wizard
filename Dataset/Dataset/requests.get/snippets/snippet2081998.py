import requests
import json
import pytz
from datetime import datetime, timedelta
from .auth import get_headers
from .ids import WDW_ID, DLR_ID


def get_advisories(self):
    '\n        Gets all the advisories for the venue and returns a list in the form of [{id, name}].\n        May take some time because it has to go to every link for each advisory.\n        '
    advisories = []
    for i in range(len(self.__data['advisories'])):
        data = requests.get(self.__data['advisories'][i]['links']['self']['href'], headers=get_headers()).json()
        this = {}
        this['id'] = data['id']
        this['name'] = data['name']
        advisories.append(this)
    return advisories
