import requests
import json
from datetime import datetime, timedelta
import pytz
from .auth import get_headers
from .parks import Park
from .pointsofinterest import PointOfInterest
from .ids import themeparkapi_ids, WDW_ID, DLR_ID
from .characters import Character


def get_associated_characters(self):
    '\n        Returns a list of associated characters Character objects\n        '
    from .characters import Character
    chars = []
    s = requests.get('https://api.wdpro.disney.go.com/global-pool-override-B/facility-service/associated-characters/{};entityType={}'.format(self.__id, self.__entityType), headers=get_headers())
    data = json.loads(s.content)
    for i in range(len(data['entries'])):
        try:
            chars.append(Character(data['entries'][i]['links']['self']['href'].split('/')[(- 1)]))
        except:
            pass
    return chars
