from calendar import day_abbr
from croniter import croniter
from datetime import datetime
from datetime import timedelta
from logging import error
from logging import info
from PIL import Image
from PIL.ImageDraw import Draw
from artwork import Artwork
from google_calendar import GoogleCalendar
from graphics import draw_text
from graphics import SCREENSTAR_SMALL_REGULAR
from city import City
from commute import Commute
from content import ContentError
from content import ImageContent
from everyone import Everyone
from firestore import DataError
from local_time import LocalTime
from sun import Sun
from wittgenstein import Wittgenstein


def delay(self, user):
    'Calculates the delay in milliseconds to the next schedule entry.'
    try:
        time = self._local_time.now(user)
    except DataError as e:
        raise ContentError(e)
    entries = [(self._next(entry['start'], time, user), entry) for entry in user.get('schedule')]
    if (not entries):
        raise ContentError('Empty schedule')
    (next_datetime, next_entry) = min(entries, key=(lambda x: x[0]))
    seconds = (next_datetime - time).total_seconds()
    seconds += DELAY_BUFFER_S
    milliseconds = int((seconds * 1000))
    info(('Using time from schedule entry: %s (%s, %s, in %d ms)' % (next_entry['name'], next_entry['start'], next_datetime.strftime('%A %B %d %Y %H:%M:%S %Z'), milliseconds)))
    return milliseconds
