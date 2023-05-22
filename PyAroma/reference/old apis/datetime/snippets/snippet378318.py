import logging
import re
import time
from datetime import datetime
from messaging import EventDrivenMessageProcessor
from serial_conn import SerialConn
from threading_more import intercept_exit_signal


@edmp.register_hook()
def sync_time_handler(force=False):
    "\n    Synchronizes the system clock with the EC2X device.\n\n    Optional arguments:\n      - force (bool): Default is 'False'.\n    "

    def get_clock_status():
        '\n        Ensures following keys for return value:\n\n        clock_synced: boolean\n        npt_enabled: boolean\n        '
        ret = {}
        res = __salt__['clock.status']()
        if ('ntp_synchronized' in res):
            ret['clock_synced'] = (res['ntp_synchronized'] == 'yes')
        elif ('system_clock_synchronized' in res):
            ret['clock_synced'] = (res['system_clock_synchronized'] == 'yes')
        else:
            raise KeyError('Could not find clock synchronization key-value pair')
        if ('network_time_on' in res):
            ret['ntp_enabled'] = (res['network_time_on'] == 'yes')
        elif ('ntp_service' in res):
            ret['ntp_enabled'] = (res['ntp_service'] == 'active')
        else:
            raise KeyError('Could not find NTP service key-value pair')
        return ret
    ret = {}
    ctx = context['time']
    if (ctx['state'] == 'synced'):
        log.info('System time has already been synchronized')
        return ret
    status = get_clock_status()
    if ((not force) and status['clock_synced']):
        log.info('System time is already NTP synchronized')
        ret['source'] = 'ntp'
        ctx['state'] = 'synced'
    else:
        if (not status['clock_synced']):
            log.info('System time is not NTP synchronized')
        if status['ntp_enabled']:
            __salt__['clock.ntp'](enable=False)
        try:
            time = None
            res = _exec('AT+CCLK?')
            if (not ('error' in res)):
                match = rtc_time_regex.match(res['data'])
                if match:
                    time = '{year:}-{month:}-{day:} {hour:}:{minute:}:{second:}'.format(**match.groupdict())
                    if (abs((datetime.utcnow() - datetime.strptime(time, '%y-%m-%d %H:%M:%S')).days) > 365):
                        log.info("Skipping invalid time retrieved from module's RTC: {:}".format(time))
                        time = None
                    else:
                        ret['source'] = 'rtc'
                else:
                    log.warning("Failed to match time result from module's RTC: {:}".format(res['data']))
            else:
                log.warning("Unable to retrieve time from module's RTC: {:}".format(res['error']))
            if (time == None):
                res = _exec('AT+QLTS=1')
                if ('error' in res):
                    raise Exception('Unable to retrieve module network time: {:}'.format(res['error']))
                match = network_time_regex.match(res['data'])
                if (not match):
                    raise Exception('Failed to match time result from module network: {:}'.format(res['data']))
                time = '{year:}-{month:}-{day:} {hour:}:{minute:}:{second:}'.format(**match.groupdict())
                ret['source'] = 'network'
            ret['old'] = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
            __salt__['clock.set'](time, adjust_system_clock=True)
            ret['new'] = time
            log.info("Synchronized system time with time from module source '{:}'".format(ret['source']))
            ctx['state'] = 'synced'
        except:
            if (ctx['state'] != 'uncertain'):
                ctx['state'] = 'uncertain'
                edmp.trigger_event({}, 'system/time/{:}'.format(ctx['state']))
            raise
        finally:
            __salt__['clock.ntp'](enable=True)
    edmp.trigger_event(ret, 'system/time/{:}'.format(ctx['state']))
    if (ret['source'] != 'rtc'):
        res = _exec('AT+CCLK="{0:%y/%m/%d,%H:%M:%S}+00"'.format(datetime.utcnow()))
        if (not ('error' in res)):
            log.info("Updated time of module's RTC")
        else:
            log.warning("Unable to update time of module's RTC: {:}".format(res['error']))
    return ret
