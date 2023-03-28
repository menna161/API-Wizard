import croniter
import logging
import salt.exceptions
import salt_more
import time
from common_util import dict_get, fromisoformat
from datetime import datetime, timedelta


def timers():
    res = __salt__['schedule.list'](return_yaml=False)
    ret = {k: dict(v, _stamp=datetime.utcnow().isoformat(), job_args=v.pop('args', []), job_kwargs=v.pop('kwargs', {})) for (k, v) in res.iteritems() if k.startswith('_sleep_timer')}
    return ret
