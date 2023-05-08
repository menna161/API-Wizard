from deribit_api import RestClient
import websocket
import json
import archon.config as config
from datetime import datetime


def on_message(ws, message):
    cur = datetime.now()
    since = (cur - start)
    m = message
    j = json.loads(m)
    if ('notifications' in j.keys()):
        n = j['notifications'][0]
        mtype = n['message']
        r = n['result']
        instr = r['instrument']
        if (instr not in mtype_count.keys()):
            mtype_count[instr] = 0
        mtype_count[instr] += 1
        print(instr, ' ', mtype_count[instr], ' ', since)
        print(n)
