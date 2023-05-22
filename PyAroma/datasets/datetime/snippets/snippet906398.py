from datetime import datetime


def day_of_year(now=datetime.now()):
    day_of_the_year = (now - datetime((now.year - 1), 12, 31))
    date_summary = ('Today is day number %d of the year %d.\n' % (day_of_the_year.days, now.year))
    return date_summary
