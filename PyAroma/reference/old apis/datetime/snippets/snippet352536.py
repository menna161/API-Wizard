from __future__ import print_function
import httplib2
import re
import os
import sys
import datetime
from functools import total_ordering
import dateutil.parser
import pytz
from jira.exceptions import JIRAError
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


def _convert_to_datestring(datestr, conf):
    return (datetime.datetime.strptime(datestr, '%Y-%m-%d').isoformat() + conf.TIMEZONE)
