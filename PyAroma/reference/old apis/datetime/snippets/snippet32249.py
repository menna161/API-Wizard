from workflow import Workflow3
from workflow.workflow3 import Item3
from settings import get_login, get_password, get_regex, get_server
import calendar
from datetime import datetime, timedelta
import logging
import logging.handlers
import os
import dateutil.parser
import pytz
import dateutil.parser
import pytz
import re


def process_google_event(self, event):
    wf = self.wf
    'Process google calendar events - sorting should be done by UID'
    import dateutil.parser
    import pytz
    try:
        startdt = event['start'].get('dateTime')
        enddt = event['end']['dateTime']
    except KeyError:
        startdt = (event['start'].get('date') + 'T00:00:00.000Z')
        enddt = (event['end']['date'] + 'T23:59:59.000Z')
    start_dateutil = dateutil.parser.parse(startdt)
    start = start_dateutil.strftime('%I:%M %p')
    end_dateutil = dateutil.parser.parse(enddt)
    end = end_dateutil.strftime('%I:%M %p')
    hide_all_day_events = (os.environ.get('hideAllDay', False) in ('1', True, 'true', 'True'))
    duration = (end_dateutil - start_dateutil)
    if (duration.days == 1):
        all_day_event = True
        time_string = 'All day Event'
        if hide_all_day_events:
            return
    else:
        all_day_event = False
        time_string = ((start + ' - ') + end)
    subtitle = time_string
    title = event.get('summary', 'No Title')
    url = event['htmlLink']
    try:
        loc = event['location']
        subtitle = (((subtitle + ' [') + loc) + ']')
    except:
        loc = ''
        pass
    body_html = event.get('description', 'No description given')
    creator = event.get('creator')
    org_name = creator.get('displayName', '')
    org_email = creator.get('email', '')
    organizer_html = (((org_name + ' &lt;') + org_email) + '&gt;')
    start_datetime = datetime.strptime(startdt.split('T')[0], '%Y-%m-%d')
    id = str(event.get('etag').replace('"', ''))
    description_url = self.write_html_template(id, title, organizer_html, start_datetime.strftime('%b'), start_datetime.strftime('%d'), time_string, loc, body_html)
    now = datetime.now(pytz.utc)
    if ((dateutil.parser.parse(enddt) < now) and (not all_day_event)):
        self.PAST_ITEMS.append(Item3(title, subtitle, arg=url, quicklookurl=description_url, type=u'file', valid=True, icon='img/eventGoogleGray.png'))
    else:
        iconfile = (('img/googleEvent_' + str(event.get('color', 1))) + '.png')
        self.FUTURE_ITEMS.append(Item3(title, subtitle, arg=url, quicklookurl=description_url, icon=iconfile, valid=True))
        try:
            hangout_url = event['hangoutLink']
            hangout_title = u'↪ Join Hangout'
            hangout_subtitle = ('        ' + hangout_url)
            self.FUTURE_ITEMS.append(Item3(hangout_title, hangout_subtitle, arg=hangout_url, valid=True, icon='img/hangout.png'))
        except:
            pass
