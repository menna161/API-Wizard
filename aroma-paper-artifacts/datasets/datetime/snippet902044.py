import time
import datetime
from .. import DeenPlugin


def unprocess(self, data):
    super(DeenPluginUnixTimestamp, self).unprocess(data)
    try:
        data = datetime.datetime.fromtimestamp(int(data)).strftime('%Y-%m-%d %H:%M:%S')
        data = data.encode()
    except (UnboundLocalError, ValueError) as e:
        self.error = e
        self.log.error(self.error)
        self.log.debug(self.error, exc_info=True)
    return data
