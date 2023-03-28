from workflow import Workflow3, ICON_INFO
from settings import get_login, get_password, get_regex, get_server, get_value_from_settings_with_default_boolean
import sys, os
from workflow.background import run_in_background, is_running
from sets import Set
import subprocess
from today import get_cache_key
from lib.pyexchange import Exchange2010Service, ExchangeBasicAuthConnection, ExchangeNTLMAuthConnection
import pytz
from pytz import timezone
from datetime import timedelta, datetime
from settings import get_value_from_settings_with_default_boolean, get_value_from_settings_with_default_int
import time


def main(wf):
    log.debug('BG EXCHANGE: STARTED')
    import pytz
    from pytz import timezone
    from datetime import timedelta, datetime
    from settings import get_value_from_settings_with_default_boolean, get_value_from_settings_with_default_int
    import time
    query = None
    if len(wf.args):
        query = wf.args[0]
    log.debug('BG: query : {!r}'.format(query))
    if (len(wf.args) > 1):
        args = wf.args
        wf.logger.debug(args)
        start_param = args[0]
        end_param = args[1]
        date_offset = args[2]
        format = '%Y-%m-%d-%H:%M:%S'
        start_outlook = datetime.strptime(start_param, format)
        end_outlook = datetime.strptime(end_param, format)
    else:
        date_offset = 0
        morning = timezone('US/Eastern').localize((datetime.today().replace(hour=0, minute=0, second=1) + timedelta(days=date_offset)))
        night = timezone('US/Eastern').localize((datetime.today().replace(hour=23, minute=59, second=59) + timedelta(days=date_offset)))
        start_outlook = morning.astimezone(pytz.utc)
        end_outlook = night.astimezone(pytz.utc)

    def wrapper():
        'A wrapper around doing an exchange server query'
        return query_exchange_server(wf, start_outlook, end_outlook, date_offset)
    cache_key = get_cache_key('exchange', date_offset)
    notify_key = cache_key.replace('exchange.', '')
    log.debug(('-- BG: CacheKey  (exchange)   ' + cache_key))
    log.debug(('-- BG: NotifyKey (exchange)   ' + notify_key))
    old_events = wf.cached_data(cache_key, max_age=0)
    new_events = wrapper()
    wf.cache_data(cache_key, new_events)
    if (old_events is None):
        wf.logger.debug('**BG --- Exchange Old: None')
    if (new_events is None):
        wf.logger.debug('**BG --- Exchange New: None')
    if (new_events is not None):
        new_set = set(map((lambda event: serialize_event(event)), new_events))
    else:
        new_set = set()
    if (old_events is not None):
        old_set = set(map((lambda event: serialize_event(event)), old_events))
    else:
        old_set = set()
    cmd = (('tell application "Alfred 3" to run trigger "NotifyOfUpdate" in workflow "org.jeef.today" with argument "' + notify_key) + '"')
    number_of_changed_events = len(new_set.symmetric_difference(old_set))
    log.debug(('-- BG: Changed Event Count: ' + str(number_of_changed_events)))
    if (number_of_changed_events > 0):
        wf.logger.debug('BG -- Exchange: ** Refresh required ')
        wf.logger.debug((('BG -- Exchange: ' + str(number_of_changed_events)) + ' events changed'))
        asrun(cmd)
