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


def _next(self, cron, after, user):
    'Finds the next time matching the cron expression.'
    try:
        cron = self._sun.rewrite_cron(cron, after, user)
    except DataError as e:
        raise ContentError(e)
    try:
        return croniter(cron, after).get_next(datetime)
    except ValueError as e:
        raise ContentError(e)
