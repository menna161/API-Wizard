import requests
import json
import pytz
from datetime import datetime, timedelta
from .auth import get_headers
from .ids import themeparkapi_ids, WDW_ID, DLR_ID


def get_hours(self, date=''):
    '\n        Gets the object\'s hours on a specific day and returns them as a datetime object.\n        Returns the object\'s hours in the following order: operating open, operating close, Extra Magic open, Extra Magic close.\n        Extra Magic hours will return None if there are none for today.\n        If all hours are None then Disney has no hours for that day.\n        date = "YYYY-MM-DD"\n        If you don\'t pass a date, it will get today\'s hours\n        '
    if (date == ''):
        DATE = datetime.today()
    else:
        (year, month, day) = date.split('-')
        DATE = datetime(int(year), int(month), int(day))
    s = requests.get('https://api.wdpro.disney.go.com/facility-service/schedules/{}?date={}-{}-{}'.format(self.__id, DATE.year, self.__formatDate(str(DATE.month)), self.__formatDate(str(DATE.day))), headers=get_headers())
    data = json.loads(s.content)
    operating_hours_start = None
    operating_hours_end = None
    extra_hours_start = None
    extra_hours_end = None
    try:
        for i in range(len(data['schedules'])):
            if (data['schedules'][i]['type'] == 'Operating'):
                operating_hours_start = datetime(DATE.year, DATE.month, DATE.day, int(data['schedules'][i]['startTime'][0:2]), int(data['schedules'][i]['startTime'][3:5]))
                if ((int(data['schedules'][i]['endTime'][0:2]) >= 0) and (int(data['schedules'][i]['endTime'][0:2]) <= 7)):
                    DATETEMP = (DATE + timedelta(days=1))
                    operating_hours_end = datetime(DATETEMP.year, DATETEMP.month, DATETEMP.day, int(data['schedules'][i]['endTime'][0:2]), int(data['schedules'][i]['endTime'][3:5]))
                else:
                    operating_hours_end = datetime(DATE.year, DATE.month, DATE.day, int(data['schedules'][i]['endTime'][0:2]), int(data['schedules'][i]['endTime'][3:5]))
            if (data['schedules'][i]['type'] == 'Special Ticketed Event'):
                extra_hours_start = datetime(DATE.year, DATE.month, DATE.day, int(data['schedules'][i]['startTime'][0:2]), int(data['schedules'][i]['startTime'][3:5]))
                if ((int(data['schedules'][i]['endTime'][0:2]) >= 0) and (int(data['schedules'][i]['endTime'][0:2]) <= 7)):
                    DATETEMP = (DATE + timedelta(days=1))
                    extra_hours_end = datetime(DATETEMP.year, DATETEMP.month, DATETEMP.day, int(data['schedules'][i]['endTime'][0:2]), int(data['schedules'][i]['endTime'][3:5]))
                else:
                    operating_hours_end = datetime(DATE.year, DATE.month, DATE.day, int(data['schedules'][i]['endTime'][0:2]), int(data['schedules'][i]['endTime'][3:5]))
    except KeyError:
        pass
    return (operating_hours_start, operating_hours_end, extra_hours_start, extra_hours_end)
