from datetime import datetime


def _day(self):
    return datetime.now().strftime('%A')
