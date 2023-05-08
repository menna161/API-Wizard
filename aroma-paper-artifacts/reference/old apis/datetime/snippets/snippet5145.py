from calendar import Calendar
from calendar import monthrange
from calendar import SUNDAY
from collections import Counter
from datetime import datetime
from datetime import timedelta
from dateutil.parser import parse
from googleapiclient import discovery
from googleapiclient.http import build_http
from logging import warning
from logging import error
from oauth2client.client import HttpAccessTokenRefreshError
from PIL import Image
from PIL.ImageDraw import Draw
from firestore import DataError
from firestore import GoogleCalendarStorage
from graphics import draw_text
from graphics import SUBVARIO_CONDENSED_MEDIUM
from content import ContentError
from content import ImageContent
from local_time import LocalTime


def _event_counts(self, time, user):
    'Retrieves a daily count of events using the Google Calendar API.'
    storage = GoogleCalendarStorage(user.id)
    credentials = storage.get()
    if (not credentials):
        error('No valid Google Calendar credentials.')
        return Counter()
    authed_http = credentials.authorize(http=build_http())
    service = discovery.build(API_NAME, API_VERSION, http=authed_http, cache_discovery=False)
    first_date = time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    (_, last_day) = monthrange(time.year, time.month)
    last_date = first_date.replace(day=last_day)
    page_token = None
    event_counts = Counter()
    while True:
        request = service.events().list(calendarId=CALENDAR_ID, timeMin=first_date.isoformat(), timeMax=last_date.isoformat(), singleEvents=True, pageToken=page_token)
        try:
            response = request.execute()
        except HttpAccessTokenRefreshError as e:
            warning(('Google Calendar request failed: %s' % e))
            return Counter()
        for event in response['items']:
            try:
                start = parse(event['start']['dateTime'])
                end = parse(event['end']['dateTime'])
                for day in self._days_range(start, end):
                    event_counts[day] += 1
            except KeyError:
                pass
            try:
                start = datetime.strptime(event['start']['date'], '%Y-%m-%d')
                end = datetime.strptime(event['end']['date'], '%Y-%m-%d')
                for day in self._days_range(start, end):
                    event_counts[day] += 1
            except KeyError:
                pass
        page_token = response.get('nextPageToken')
        if (not page_token):
            break
    return event_counts
