import time
import datetime
from .. import DeenPlugin


def process(self, data):
    super(DeenPluginUnixTimestamp, self).process(data)
    try:
        data = str(int(time.mktime(datetime.datetime.strptime(''.join(map(chr, data.strip())), '%Y-%m-%d %H:%M:%S').timetuple())))
        data = data.encode()
    except ValueError as e:
        self.error = e
        self.log.error(self.error)
        self.log.debug(self.error, exc_info=True)
    return data
