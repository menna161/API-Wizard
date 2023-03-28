import datetime
import json
import logging
import os
from salt.returners import get_returner_options


def returner_data(data, *args, **kwargs):
    '\n    Return any arbitrary data structure to a JSONL file.\n    '
    if (not data):
        log.debug('Skipping empty data result')
        return
    now = datetime.datetime.utcnow().isoformat()
    if isinstance(data, dict):
        payload = data
    elif isinstance(data, (list, set, tuple)):
        payload = {'_stamp': now, 'values': data}
    else:
        payload = {'_stamp': now, 'value': data}
    if args:
        payload['_type'] = '.'.join([str(t) for t in (list(args) + [payload.get('_type', None)]) if t])
    options = _get_options(kwargs)
    format_kwargs = dict(now=now, uid=__opts__['id'], pid=os.getpid())
    directory = options['dir'].format(**format_kwargs)
    filename = options['filename'].format(**format_kwargs)
    with open(os.path.join(directory, filename), options['mode']) as file:
        file.write((json.dumps(payload, separators=(',', ':')) + '\n'))
