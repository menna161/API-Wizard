import requests
import pytz
from datetime import datetime, timedelta
from .auth import get_headers
from .ids import WDW_ID, DLR_ID


def __init__(self, id=None):
    '\n        Constructor Function\n        Gets all points of interest data available and stores various elements into variables.\n        '
    error = True
    self.__data = requests.get('https://api.wdpro.disney.go.com/global-pool-override-B/facility-service/points-of-interest/{}'.format(id), headers=get_headers()).json()
    try:
        if (self.__data['id'] is not None):
            error = False
    except:
        pass
    if error:
        raise ValueError(('That point of interest is not available. id: ' + str(id)))
    self.__id = id
    self.__name = self.__data['name']
    self.__entityType = self.__data['type']
    try:
        self.__subType = self.__data['subType']
    except:
        self.__subType = None
    try:
        self.__anc_dest_id = self.__data['ancestorDestination']['id'].split(';')[0]
    except:
        self.__anc_dest_id = None
    try:
        self.__anc_park_id = self.__data['links']['ancestorThemePark']['href'].split('/')[(- 1)].split('?')[0]
    except:
        try:
            self.__anc_park_id = self.__data['links']['ancestorWaterPark']['href'].split('/')[(- 1)].split('?')[0]
        except:
            try:
                self.__anc_park_id = self.__data['ancestorThemeParkId'].split(';')[0]
            except:
                try:
                    self.__anc_park_id = self.__data['ancestorWaterParkId'].split(';')[0]
                except:
                    self.__anc_park_id = None
    try:
        self.__anc_resort_id = self.__data['links']['ancestorResort']['href'].split('/')[(- 1)].split('?')[0]
    except:
        try:
            self.__anc_resort_id = self.__data['ancestorResortId'].split(';')[0]
        except:
            self.__anc_resort_id = None
    try:
        self.__anc_land_id = self.__data['links']['ancestorLand']['href'].split('/')[(- 1)].split('?')[0]
    except:
        try:
            self.__anc_land_id = self.__data['ancestorLandId'].split(';')[0]
        except:
            self.__anc_land_id = None
    try:
        self.__anc_ra_id = self.__data['links']['ancestorResortArea']['href'].split('/')[(- 1)].split('?')[0]
    except:
        try:
            self.__anc_ra_id = self.__data['ancestorResortAreaId'].split(';')[0]
        except:
            self.__anc_ra_id = None
    try:
        self.__anc_ev_id = self.__data['links']['ancestorEntertainmentVenue']['href'].split('/')[(- 1)].split('?')[0]
    except:
        try:
            self.__anc_ev_id = self.__data['ancestorEntertainmentVenueId'].split(';')[0]
        except:
            self.__anc_ev_id = None
    if (self.__anc_dest_id == WDW_ID):
        self.__time_zone = pytz.timezone('US/Eastern')
    elif (self.__anc_dest_id == DLR_ID):
        self.__time_zone = pytz.timezone('US/Pacific')
    else:
        self.__time_zone = pytz.utc
