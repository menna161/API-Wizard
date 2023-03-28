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


def image(self, user, width, height, variant):
    'Generates the current image based on the schedule.'
    try:
        time = self._local_time.now(user)
    except DataError as e:
        raise ContentError(e)
    today = time.replace(hour=0, minute=0, second=0, microsecond=0)
    while True:
        entries = [(self._next(entry['start'], today, user), entry) for entry in user.get('schedule')]
        if (not entries):
            raise ContentError('Empty schedule')
        past_entries = list(filter((lambda x: (x[0] <= time)), entries))
        if past_entries:
            (latest_datetime, latest_entry) = max(past_entries, key=(lambda x: x[0]))
            break
        today -= timedelta(days=1)
    info(('Using image from schedule entry: %s (%s, %s)' % (latest_entry['name'], latest_entry['start'], latest_datetime.strftime('%A %B %d %Y %H:%M:%S %Z'))))
    image = self._image(latest_entry['image'], user, width, height, variant)
    return image
