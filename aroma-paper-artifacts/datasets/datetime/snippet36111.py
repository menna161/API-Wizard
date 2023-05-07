import logging


def duration(self):
    'Returns time duration as datetime.TimeDelta, or None if infinite.'
    if ((self.start is None) or (self.end is None)):
        return None
    return (self.end - self.start)
