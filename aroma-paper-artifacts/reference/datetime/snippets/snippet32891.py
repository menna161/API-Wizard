import sys
from query_exchange import asrun, asquote
from workflow import Workflow3, ICON_INFO
from today import get_cache_key
import GoogleInterface
from GoogleInterface import GoogleInterface, NoCalendarException
import pytz
from pytz import timezone
from datetime import timedelta, datetime
from settings import get_value_from_settings_with_default_boolean, get_value_from_settings_with_default_int
import time


def main(wf):
    log.debug('BG GOOGLE: STARTED')
    import pytz
    from pytz import timezone
    from datetime import timedelta, datetime
    from settings import get_value_from_settings_with_default_boolean, get_value_from_settings_with_default_int
    import time
    query = None
    if len(wf.args):
        query = wf.args[0]
    log.debug('BG: query : {!r}'.format(query))
    args = wf.args
    if (len(wf.args) > 1):
        wf.logger.debug(args)
        start_google = args[0]
        stop_google = args[1]
        date_offset = args[2]
    else:
        date_offset = 0
        morning = timezone('US/Eastern').localize((datetime.today().replace(hour=0, minute=0, second=1) + timedelta(days=date_offset)))
        night = timezone('US/Eastern').localize((datetime.today().replace(hour=23, minute=59, second=59) + timedelta(days=date_offset)))
        start_google = morning.astimezone(pytz.utc).isoformat()
        stop_google = night.astimezone(pytz.utc).isoformat()

    def wrapper():
        'A wrapper around doing a google query so this can be used with a cache function'
        return query_google_calendar(wf, start_google, stop_google, date_offset)
    cache_key = get_cache_key('google', date_offset)
    notify_key = cache_key.replace('google.', '')
    log.debug(('-- BG: CacheKey  (Google)   ' + cache_key))
    log.debug(('-- BG: NotifyKey (Google)   ' + notify_key))
    old_events = wf.cached_data(cache_key, max_age=0)
    new_events = wrapper()
    wf.cache_data(cache_key, new_events)
    if (old_events is None):
        wf.logger.debug('**BG --- Google Old: None')
    else:
        for o in old_events:
            wf.logger.debug(' '.join(['**BG --- Google Old:', str(o['start']), o.get('summary', 'NoTitle')]))
    if (new_events is None):
        wf.logger.debug('**BG --- Google New: None')
    else:
        for n in new_events:
            wf.logger.debug(' '.join(['**BG --- Google New:', str(n['start']), n.get('summary', 'NoTitle')]))

    def lambda_func(x):
        return ':'.join([x['id'], x['updated'], str(x.get(u'start').get(u'dateTime', 'All_Day'))])
    if (new_events is not None):
        new_set = set(map((lambda x: lambda_func(x)), new_events))
    else:
        new_set = set()
    if (old_events is not None):
        old_set = set(map((lambda x: lambda_func(x)), old_events))
    else:
        old_set = set()
    wf.logger.debug(('Old Set: ' + str(old_set)))
    wf.logger.debug(('New Set: ' + str(new_set)))
    cmd = (('tell application "Alfred 3" to run trigger "NotifyOfUpdate" in workflow "org.jeef.today" with argument "' + notify_key) + '"')
    number_of_changed_events = len(new_set.symmetric_difference(old_set))
    log.debug(('-- BG: Changed Event Count: ' + str(number_of_changed_events)))
    if (number_of_changed_events > 0):
        wf.logger.debug('BG -- Google: ** Refresh required ')
        wf.logger.debug((('BG -- Google: ' + str(number_of_changed_events)) + ' events changed'))
        evts = wf.cached_data(cache_key, max_age=0)
        for e in evts:
            wf.logger.debug(' '.join(['**BG --- Google:', str(e['start']), e.get('summary', 'NoTitle')]))
            wf.logger.debug(('BG -- Google: ' + cmd))
        asrun(cmd)
    log.debug('--- TERMINATING --')
