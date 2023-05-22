import requests
import json
from datetime import datetime, timedelta
import pytz
from .auth import get_headers
from .parks import Park
from .pointsofinterest import PointOfInterest
from .ids import themeparkapi_ids, WDW_ID, DLR_ID
from .characters import Character


def get_number_associated_characters(self):
    '\n        Gets the total number of characters associated with this object\n        '
    s = requests.get('https://api.wdpro.disney.go.com/global-pool-override-B/facility-service/associated-characters/{};entityType={}'.format(self.__id, self.__entityType), headers=get_headers())
    data = json.loads(s.content)
    return data['total']
