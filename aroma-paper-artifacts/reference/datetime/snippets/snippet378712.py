import datetime
import logging
import re
import salt.exceptions


def boot_time():
    '\n    Get timestamp for last boot of system.\n    '
    ret = {'value': None}
    res = __salt__['cmd.shell']("grep 'Booting Linux' /var/log/syslog | tail -1")
    if (not res):
        return ret
    match = _linux_boot_log_regex.match(res)
    if (not match):
        raise salt.exceptions.CommandExecutionError('Unable to parse log line: {:}'.format(res))
    now = datetime.datetime.now()
    last_off = datetime.datetime.strptime(match.group('timestamp'), '%b %d %H:%M:%S').replace(year=now.year)
    if (last_off > now):
        last_off = last_off.replace(year=(now.year - 1))
    ret['value'] = last_off.isoformat()
    return ret
