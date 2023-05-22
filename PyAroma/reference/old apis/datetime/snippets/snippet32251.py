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


def process_outlook_event(self, event):
    'Reads and processes an outlook event.  The UID field will be responsible for handling the sorting inside of Alfred'
    import re
    REGEX = get_regex(self.wf)
    id = str(event.id).replace('+', '').replace('/', '')
    location = (event.location or 'No Location Specified')
    subject = (event.subject or 'No Subject')
    start_datetime = self.utc_to_local(event.start)
    end_datetime = self.utc_to_local(event.end)
    body_html = event.html_body
    time_string = ((start_datetime.strftime('%I:%M %p') + ' - ') + end_datetime.strftime('%I:%M %p'))
    org_name = event.organizer[0]
    org_email = event.organizer[1]
    organizer_html = (((org_name + ' &lt;') + org_email) + '&gt;')
    if body_html:
        description_url = self.write_html_template(id, subject, organizer_html, start_datetime.strftime('%b'), start_datetime.strftime('%d'), time_string, location, body_html)
    else:
        description_url = ''
    online_meeting_url = None
    if REGEX:
        self.wf.logger.info(('Regex: ' + REGEX))
    else:
        self.wf.logger.info('Regex: None')
    self.wf.logger.info(body_html)
    if (not (REGEX is None)):
        p = re.compile(REGEX)
        if body_html:
            match = re.search(p, body_html)
            if match:
                online_meeting_url = match.group(1)
    title = subject
    subtitle = time_string
    if location:
        subtitle += ((' [' + location) + ']')
    subtitle += ' hit shift for details'
    now = datetime.now()
    if (end_datetime < now):
        self.PAST_ITEMS.append(Item3(title, subtitle, type=u'file', arg=description_url, valid=False, icon='img/eventOutlookGray.png'))
    else:
        hide_all_day_events = (os.environ.get('hideAllDay', False) in ('1', True, 'true', 'True'))
        if event.is_all_day:
            if hide_all_day_events:
                pass
            else:
                self.FUTURE_ITEMS.append(Item3(title, subtitle, type=u'file', arg=description_url, valid=False, icon='img/eventOutlook.png'))
        else:
            self.FUTURE_ITEMS.append(Item3(title, subtitle, type=u'file', arg=description_url, valid=False, icon='img/eventOutlook.png'))
        if (online_meeting_url != None):
            online_meeting_img = 'img/online_meeting.png'
            online_meeting_title = u'↪ Join Meeting'
            online_meeting_subtitle = ('        ' + online_meeting_url)
            if ('chime' in online_meeting_url):
                online_meeting_img = 'img/chime.png'
                online_meeting_title = u'↪ Join Chime Meeting'
            elif ('skype' in online_meeting_url):
                online_meeting_img = 'img/skype.png'
                online_meeting_title = u'↪ Join Skype Meeting'
            self.FUTURE_ITEMS.append(Item3(online_meeting_title, online_meeting_subtitle, arg=online_meeting_url, valid=True, icon=online_meeting_img))
