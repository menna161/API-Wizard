import datetime
import logging
import salt.exceptions
import salt.utils.event
import salt.utils.jid
import time
from retrying import retry
from salt.utils.network import host_to_ips as _host_to_ips
from salt.utils.network import remote_port_tcp as _remote_port_tcp


def request_restart(pending=True, immediately=False, delay=10, expiration=1200, reason='unknown'):
    "\n    Request for a future restart of the minion service.\n\n    Optional arguments:\n      - pending (bool): Default is 'True'.\n      - immediately (bool): Default is 'False'.\n      - delay (int): Default is '10'.\n      - expiration (int): Default is '1200'.\n      - reason (str): Reason code that tells why we decided to restart. Default is 'unknown'.\n    "
    if (pending or __context__.get('minionutil.request_restart', False)):
        if immediately:
            log.warn("Performing minion restart in {:} second(s) because of reason '{:}'".format(delay, reason))
            trigger_event('system/minion/restarting', data={'reason': reason})
            time.sleep(delay)
            return __salt__['service.restart']('salt-minion')
        elif (expiration > 0):
            __salt__['schedule.add']('_restart_timer/{:}'.format(reason), function='minionutil.restart', job_kwargs={'reason': reason}, seconds=expiration, maxrunning=1, return_job=False, persist=False, metadata={'created': datetime.datetime.utcnow().isoformat(), 'transient': True})
            log.info("Pending request for minion restart because of reason '{:}' is scheduled to be performed automatically in {:} second(s)".format(reason, expiration))
        else:
            log.info("Request for minion restart is pending because of reason '{:}'".format(reason))
    else:
        log.debug('No pending minion restart request')
    __context__['minionutil.request_restart'] = pending
    return {'pending': pending}
