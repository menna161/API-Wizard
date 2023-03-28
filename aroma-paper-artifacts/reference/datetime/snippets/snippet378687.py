import croniter
import logging
import salt.exceptions
import salt_more
import time
from common_util import dict_get, fromisoformat
from datetime import datetime, timedelta


def sleep_timer(enable=None, period=1800, add=None, clear=None, refresh=None, **kwargs):
    "\n    Setup sleep timer to schedule power off upon inactivity.\n\n    NOTE: Do not access pillar data in this function as they will not be available when called from engines (separate processes).\n\n    Optional arguments:\n      - add (str): Add a timer with the given name.\n      - clear (str): Clear sleep timer(s) matching the given name. Use '*' to clear all.\n      - enable (bool): Enable or disable timer. __DEPRECATED__: Use 'add' or 'clear' instead.\n      - period (int): Timer period in seconds before performing sleep. Default is '1800'.\n      - reason (str): Reason code that tells why we decided to sleep. Default is 'unknown'.\n    "
    reason = kwargs.setdefault('reason', 'unknown')
    if (enable != None):
        log.warning("Using deprecated argument 'enable' - use 'add' or 'clear' instead")

    def timers():
        res = __salt__['schedule.list'](return_yaml=False)
        ret = {k: dict(v, _stamp=datetime.utcnow().isoformat(), job_args=v.pop('args', []), job_kwargs=v.pop('kwargs', {})) for (k, v) in res.iteritems() if k.startswith('_sleep_timer')}
        return ret
    config = {}
    try:
        config = __salt__['fileutil.load_yaml']('/opt/autopi/power/sleep_timer.yml')
    except:
        log.exception('Failed to load sleep timer configuration file')
    if ((clear != None) or (enable == False)):
        for name in timers():
            if (clear not in [None, '*']):
                if ('_sleep_timer/{:}'.format(clear) != name):
                    continue
            res = __salt__['schedule.delete'](name)
            __salt__['minionutil.trigger_event']('system/{:}/cleared'.format(name.lstrip('_')), data={'reason': reason})
    if ((add != None) or (enable == True)):
        name = '_sleep_timer/{:}'.format((add or reason))
        res = __salt__['schedule.delete'](name)
        kwargs = salt_more.clean_kwargs(kwargs)
        kwargs['confirm'] = True
        now = datetime.utcnow()
        expiry = (now + timedelta(seconds=period))
        res = __salt__['schedule.add'](name, function='power.sleep', job_kwargs=kwargs, seconds=period, maxrunning=1, return_job=False, persist=False, metadata={'created': now.isoformat(), 'expires': expiry.isoformat(), 'transient': True, 'revision': 2})
        if res.get('result', False):
            if (refresh == None):
                refresh = (add or reason)
            __salt__['minionutil.trigger_event']('system/{:}/added'.format(name.lstrip('_')), data=({'reason': reason} if (not name.endswith('/{:}'.format(reason))) else {}))
            try:
                __salt__['cmd.run']('wall -n "\nATTENTION ({:}):\n\nSleep timer \'{:}\' added which is scheduled to trigger at {:}.\nRun command \'autopi power.sleep_timer\' to list active sleep timers.\n\n(Press ENTER to continue)"'.format(now, name[(name.rindex('/') + 1):], expiry))
            except:
                log.exception('Failed to broadcast sleep timer added notification')
        else:
            log.error("Failed to add sleep timer '{:}': {:}".format(name, res))
    if (refresh != None):
        boot_delay = dict_get(config, 'suppress', 'boot_delay', default=60)
        for (name, schedule) in timers().iteritems():
            if (refresh not in [None, '*']):
                if ('_sleep_timer/{:}'.format(refresh) != name):
                    continue
            for entry in dict_get(config, 'suppress', 'schedule', default=[]):
                try:
                    if (not ('|' in entry)):
                        raise ValueError('No pipe sign separator found in schedule entry')
                    (expression, duration) = entry.split('|')
                    expiry = fromisoformat(schedule['metadata']['expires'])
                    for suppress_start in [croniter.croniter(expression.strip(), expiry).get_prev(datetime), croniter.croniter(expression.strip(), expiry).get_next(datetime)]:
                        suppress_end = (suppress_start + timedelta(seconds=int(duration.strip())))
                        sleep_start = expiry
                        sleep_end = (expiry + timedelta(seconds=(schedule['job_kwargs'].get('interval', 86400) + boot_delay)))
                        if ((sleep_start < suppress_end) and (sleep_end > suppress_start)):
                            log.info("Sleep timer '{:}' sleep period from {:} to {:} overlaps with sleep suppress period from {:} to {:}".format(name, sleep_start, sleep_end, suppress_start, suppress_end))
                            now = datetime.utcnow()
                            if ((schedule['job_kwargs'].get('interval', 0) > 0) and (sleep_start < suppress_start) and ((suppress_start - sleep_start).total_seconds() > boot_delay)):
                                state = 'reduced'
                                old_interval = schedule['job_kwargs']['interval']
                                new_interval = int(((suppress_start - sleep_start).total_seconds() - boot_delay))
                                log.warning("Reducing sleeping time of sleep timer '{:}' from {:} to {:} seconds due to suppress schedule: {:}".format(name, old_interval, new_interval, entry))
                                schedule['job_kwargs']['interval'] = new_interval
                                schedule['seconds'] = (expiry - now).total_seconds()
                            else:
                                state = 'postponed'
                                old_period = schedule['seconds']
                                new_period = (suppress_end - now).total_seconds()
                                log.warning("Postponing sleep timer '{:}' from {:} to {:} seconds due to suppress schedule: {:}".format(name, old_period, new_period, entry))
                                schedule['seconds'] = new_period
                            expiry = (now + timedelta(seconds=schedule['seconds']))
                            schedule['metadata']['updated'] = now.isoformat()
                            schedule['metadata']['expires'] = expiry.isoformat()
                            res = __salt__['schedule.modify'](**schedule)
                            if res.get('result', False):
                                __salt__['minionutil.trigger_event']('system/{:}/{:}'.format(name.lstrip('_'), state))
                                try:
                                    __salt__['cmd.run']('wall -n "\nATTENTION ({:}):\n\nSleep timer \'{:}\' has been {:} due to sleep suppress rule and is scheduled to trigger at {:}.\nRun command \'autopi power.sleep_timer\' to list active sleep timers.\n\n(Press ENTER to continue)"'.format(now, name[(name.rindex('/') + 1):], state, expiry))
                                except:
                                    log.exception('Failed to broadcast sleep timer modified notification')
                            else:
                                log.error("Failed to modify sleep timer '{:}': {:}".format(name, res))
                        elif log.isEnabledFor(logging.DEBUG):
                            log.debug("Sleep timer '{:}' does not overlap with suppress schedule: {:}".format(name, entry))
                except:
                    log.exception("Failed to process suppress schedule for sleep timer '{:}': {:}".format(name, entry))
    return timers()
