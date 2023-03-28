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


def _days_range(self, start, end):
    'Returns a list of days of the month between two datetimes.'
    end -= timedelta(microseconds=1)
    return range(start.day, (end.day + 1))
