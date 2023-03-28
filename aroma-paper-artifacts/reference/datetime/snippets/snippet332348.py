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


def get_observations_from_baseline():
    dn = sys.argv[1]
    fn = os.path.join(dn, 'baseline.json')
    if (not os.path.exists(fn)):
        raise Exception(('%s does not exist' % fn))
    logger.info(('reading %s' % fn))
    with open(fn, 'r') as f:
        baseline = json.loads(f.read())
    observations = []
    obs = {'host': None, 'ts': baseline[0]['play']['duration']['start'], 'task_name': None}
    observations.append(obs)
    for task in baseline[0]['tasks']:
        tn = task['task']['name']
        for (hn, hd) in task['hosts'].items():
            for key in ['start', 'end']:
                obs = {'task_name': tn, 'host': hn, 'ts': hd['duration'][key]}
                observations.append(obs)
    obs = {'host': None, 'ts': baseline[0]['play']['duration']['end'], 'task_name': None}
    observations.append(obs)
    for (idx, x) in enumerate(observations):
        ts = x['ts']
        ts = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%f')
        ts = ts.timestamp()
        observations[idx]['ts'] = ts
    observations = sorted(observations, key=(lambda x: x['ts']))
    return observations
