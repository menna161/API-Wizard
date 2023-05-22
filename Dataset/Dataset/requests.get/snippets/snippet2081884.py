import json
from datetime import datetime, timedelta
import requests
import pytz
from .auth import get_headers
from .ids import themeparkapi_ids, WDW_ID, DLR_ID
from .characters import Character


def check_associated_characters(self):
    '\n        Checks if object has any associated characters\n        '
    s = requests.get('https://api.wdpro.disney.go.com/global-pool-override-B/facility-service/associated-characters/{};entityType={}'.format(self.__id, self.__entityType), headers=get_headers())
    data = json.loads(s.content)
    if (data['total'] > 0):
        return True
    else:
        return False
