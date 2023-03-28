import atexit
from datetime import datetime
import json
from threading import Thread
from urllib.request import Request, urlopen


def log(msg, slack=False):
    print(msg)
    if (_file is not None):
        _file.write(('[%s]  %s\n' % (datetime.now().strftime(_format)[:(- 3)], msg)))
    if (slack and (_slack_url is not None)):
        Thread(target=_send_slack, args=(msg,)).start()
