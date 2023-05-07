from datetime import datetime


def day():
    return datetime.now().strftime('%A')
