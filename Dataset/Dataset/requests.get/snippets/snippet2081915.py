import requests
from datetime import datetime, timedelta
import pytz
from .auth import get_headers
from .parks import Park
from .entertainments import Entertainment
from .attractions import Attraction
from .ids import WDW_PARK_IDS, DLR_PARK_IDS, WDW_ID, DLR_ID, DESTINATION_IDS, themeparkapi_ids


def __init__(self, id=None):
    '\n        Constructor Function\n        Allows access to various destination related data.\n        '
    error = True
    self.__data = requests.get('https://api.wdpro.disney.go.com/facility-service/destinations/{}'.format(id), headers=get_headers()).json()
    try:
        if (self.__data['id'] is not None):
            error = False
    except:
        pass
    if error:
        raise ValueError((('That destination is not available. id: ' + str(id)) + '. Available destinations: {}'.format(', '.join(DESTINATION_IDS))))
    self.__id = id
    self.__name = self.__data['name']
    self.__entityType = self.__data['type']
    if (self.__id == WDW_ID):
        self.__time_zone = pytz.timezone('US/Eastern')
    elif (self.__id == DLR_ID):
        self.__time_zone = pytz.timezone('US/Pacific')
    else:
        self.__time_zone = pytz.utc
