import time
import datetime


def avg_time_str(self):
    time_str = str(datetime.timedelta(seconds=self.average_time))
    return time_str
