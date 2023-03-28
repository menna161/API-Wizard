import datetime
import os
import json
from flask import Flask
from flask import request


@app.route('/checkpoint/<path:path>', methods=['GET', 'POST'])
def checkpoint(path):
    print(path)
    ts = get_ts()
    logfile = os.path.join(fixtures, 'entries.log')
    with open(logfile, 'a') as f:
        f.write(('%s checkpoint %s\n' % (datetime.datetime.now().isoformat(), path)))
    return ''
