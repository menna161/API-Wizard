from datetime import datetime
import time


def set_start(self, start_time_str):
    '\n        Set the match\'s start time from a formatted string.\n\n        Args:\n            start_time_str (str): String representing the match start time,\n                expected in the format of "%d %b %Y %H:%M".\n        '
    self.start = datetime.strptime(start_time_str, '%d %b %Y %H:%M')
