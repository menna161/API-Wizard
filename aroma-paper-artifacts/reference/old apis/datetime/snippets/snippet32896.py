from __future__ import print_function
import os
import sys
import httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import datetime
import argparse


def main():
    "Shows basic usage of the Google Calendar API.\n\n    Creates a Google Calendar API service object and outputs a list of the next\n    10 events on the user's calendar.\n    "
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http(disable_ssl_certificate_validation=True))
    service = discovery.build('calendar', 'v3', http=http)
    now = (datetime.datetime.utcnow().isoformat() + 'Z')
    page_token = None
    cals = service.calendarList().list(pageToken=page_token).execute()
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print('\n********************************************')
            print(((((('Name: ' + calendar_list_entry['summary']) + ' ACL: ') + calendar_list_entry['accessRole']) + '   Calendar ID: ') + calendar_list_entry['id']))
            cal_id = calendar_list_entry['id']
            print(cal_id)
            eventsResult = service.events().list(calendarId=cal_id, timeMin=now, maxResults=10, singleEvents=True, orderBy='startTime').execute()
            events = eventsResult.get('items', [])
            if (not events):
                print('No upcoming events found.')
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                print(start, event.get('summary', 'No Summary Given'))
        page_token = calendar_list.get('nextPageToken')
        if (not page_token):
            break
