from datetime import datetime


def time_alive(now=datetime.now()):
    your_life = (now - datetime(1970, 1, 1))
    len_existence = ('Today is day number %d of your life.\n' % your_life.days)
    return len_existence
