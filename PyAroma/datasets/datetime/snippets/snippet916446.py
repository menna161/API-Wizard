from __future__ import unicode_literals
import argparse
import httplib2
from apiclient.discovery import build
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from oauth2client import client
from oauth2client import GOOGLE_REVOKE_URI
from oauth2client import GOOGLE_TOKEN_URI
from six.moves import xrange
from projects.models import ProjectPage


def valid_date(self, date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        message = "Not a valid date: '{0}'.".format(date_string)
        raise argparse.ArgumentTypeError(message)
    else:
        return date_string
