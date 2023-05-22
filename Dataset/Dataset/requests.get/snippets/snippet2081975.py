import requests
import json
from datetime import datetime, timedelta
import pytz
from .auth import get_headers
from .parks import Park
from .pointsofinterest import PointOfInterest
from .ids import themeparkapi_ids, WDW_ID, DLR_ID
from .characters import Character


def get_schedule(self, date='', timestamp=False):
    '\n        Returns a list of dictionaries for the specified date\'s schedule in the form of [{start_time, end_time}]\n        date = "YYYY-MM-DD"\n        If you don\'t pass a date, it will get today\'s schedule\n        timestamp = False\n        Whether to return datetime objects or timestamps\n        '
    if (date == ''):
        DATE = datetime.today()
    else:
        (year, month, day) = date.split('-')
        DATE = datetime(int(year), int(month), int(day))
    strdate = '{}-{}-{}'.format(DATE.year, self.__formatDate(str(DATE.month)), self.__formatDate(str(DATE.day)))
    data = requests.get('https://api.wdpro.disney.go.com/facility-service/schedules/{}?date={}'.format(self.__id, strdate), headers=get_headers()).json()
    schedule = []
    try:
        for entry in data['schedules']:
            if (entry['type'] == 'Performance Time'):
                this = {}
                start_time = datetime.strptime('{} {}'.format(entry['date'], entry['startTime']), '%Y-%m-%d %H:%M:%S')
                end_time = datetime.strptime('{} {}'.format(entry['date'], entry['endTime']), '%Y-%m-%d %H:%M:%S')
                if timestamp:
                    this['start_time'] = start_time.timestamp()
                    this['end_time'] = end_time.timestamp()
                else:
                    this['start_time'] = start_time
                    this['end_time'] = end_time
                schedule.append(this)
    except Exception as e:
        pass
    return schedule
