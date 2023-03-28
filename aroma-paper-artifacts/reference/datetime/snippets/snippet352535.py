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


def import_worklogs(jira, jira_user, worklogconfig, calendar_name, from_day, to_day):
    "\n    Imports worklogs using the Google Calendar API and sumbits them to JIRA.\n    Calendar entries must start with JIRA issue IDs opitionally followed by\n    ':' and comments. Returns total hours logged as timedelta.\n    "
    if (from_day >= to_day):
        print('Start date must be before end date, start:', from_day, 'end:', to_day)
        return 0
    from_day = _convert_to_datestring(from_day, worklogconfig)
    to_day = _convert_to_datestring(to_day, worklogconfig)
    service = _get_calendar_service(worklogconfig)
    calendarId = _get_calendar_id(service, calendar_name)
    eventsResult = service.events().list(calendarId=calendarId, timeMin=from_day, timeMax=to_day, maxResults=1000, singleEvents=True, orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if (not events):
        print('No events found in calendar', calendar_name, 'during', from_day, '-', to_day)
        return 0
    durations = []
    prefix_filter = (worklogconfig.WORKLOG_PREFIX_FILTER if (hasattr(worklogconfig, 'WORKLOG_PREFIX_FILTER') and worklogconfig.WORKLOG_PREFIX_FILTER) else None)
    if prefix_filter:
        print('** Filtering worklogs by prefix', prefix_filter)
        events = [event for event in events if event['summary'].startswith(prefix_filter)]
    for event in events:
        try:
            gcal_worklog = Worklog.from_gcal(event)
            jira_worklogs = [Worklog.from_jira(w) for w in jira.worklogs(gcal_worklog.issue) if (w.author.key == jira_user)]
            if (jira_worklogs and (gcal_worklog in jira_worklogs)):
                jira_worklog = next((w for w in jira_worklogs if (w == gcal_worklog)))
                if (gcal_worklog.duration != jira_worklog.duration):
                    raise WorklogParseError(('Google worklog for issue %s starting at %s: duration %s differs from JIRA duration %s' % (gcal_worklog.issue, gcal_worklog.start, gcal_worklog.duration, jira_worklog.duration)))
                print(gcal_worklog.duration, 'hours starting', gcal_worklog.start, 'already logged for', gcal_worklog.issue)
            else:
                print('Logging', gcal_worklog.duration, 'hours starting', gcal_worklog.start, 'for', gcal_worklog.issue)
                started = gcal_worklog.start
                if worklogconfig.JIRA_TIMEZONE:
                    jira_tz = pytz.timezone(worklogconfig.JIRA_TIMEZONE)
                    started -= jira_tz.utcoffset(gcal_worklog.start.replace(tzinfo=None))
                jira.add_worklog(issue=gcal_worklog.issue, timeSpentSeconds=gcal_worklog.duration.seconds, started=started, comment=gcal_worklog.comment)
                durations.append(gcal_worklog.duration)
        except WorklogParseError as e:
            print(e)
        except JIRAError as e:
            print((("Issue '" + gcal_worklog.issue) + "' does not exist (or other JIRA error):"), e)
    return sum(durations, datetime.timedelta(0))
