import boto3
import sys
from datetime import date, datetime, timedelta
import hashlib
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import argparse
import datetime


def create_events(service, events, event_ids):
    import datetime
    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            if (calendar_list_entry['summary'] == 'aws'):
                calendar_id = calendar_list_entry['id']
        page_token = calendar_list.get('nextPageToken')
        if (not page_token):
            break
    ' Get the current events from Google Calendar'
    page_token = None
    g_event_ids = []
    while True:
        g_events = service.events().list(calendarId=calendar_id, pageToken=page_token).execute()
        for event in g_events['items']:
            g_event_ids.append(event['id'])
        page_token = g_events.get('nextPageToken')
        if (not page_token):
            break
    if (len(events) >= 1):
        print(('Creating %s events in the aws Calendar of your Google Account' % len(events)))
    n = 0
    for id in event_ids:
        if (id in g_event_ids):
            print(('The event: %s is already scheduled. Nothing to do...' % events[n]['id']))
        else:
            event = service.events().insert(calendarId=calendar_id, body=events[n]).execute()
            print(('Event created: %s' % event.get('htmlLink')))
        n += 1
