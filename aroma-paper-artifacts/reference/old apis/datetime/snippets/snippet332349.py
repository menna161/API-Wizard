import datetime
import json
import os
import sys
import time
import pytz
import svgwrite
from svgwrite import cm, mm, percent
from svgwrite import percent as pc
from logzero import logger


def get_vmstats():
    dn = sys.argv[1]
    fn = os.path.join(dn, 'vmstat.log')
    if (not os.path.exists(fn)):
        raise Exception(('%s does not exist' % fn))
    logger.info(('reading %s' % fn))
    with open(fn, 'r') as f:
        lines = f.readlines()
    rows = []
    VMSTAT_TIMEZONE = None
    for line in lines:
        cols = line.split()
        if (cols[0] == 'procs'):
            continue
        if (cols[0] == 'r'):
            VMSTAT_TIMEZONE = cols[(- 1)]
            continue
        data = {'vmstat_r': int(cols[0]), 'vmstat_b': int(cols[1]), 'vmstat_swpd': int(cols[2]), 'vmstat_free': int(cols[3]), 'vmstat_buff': int(cols[4]), 'vmstat_cache': int(cols[5]), 'vmstat_si': int(cols[6]), 'vmstat_so': int(cols[7]), 'vmstat_bi': int(cols[8]), 'vmstat_bo': int(cols[9]), 'vmstat_in': int(cols[10]), 'vmstat_cs': int(cols[11]), 'vmstat_us': int(cols[12]), 'vmstat_sy': int(cols[13]), 'vmstat_id': int(cols[14]), 'vmstat_wa': int(cols[15]), 'vmstat_st': int(cols[16])}
        ts = ((cols[17] + ' ') + cols[18])
        tstmp = datetime.datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')
        try:
            tz = getattr(pytz, VMSTAT_TIMEZONE.lower())
        except AttributeError as e:
            tz = pytz.timezone(VMSTAT_TIMEZONE.upper())
        tzts = datetime.datetime(tstmp.year, tstmp.month, tstmp.day, tstmp.hour, tstmp.minute, tstmp.second, tzinfo=tz)
        data['ts'] = tzts.timestamp()
        rows.append(data)
    return rows
