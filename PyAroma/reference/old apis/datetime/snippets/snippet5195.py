from astral import Astral
from astral import AstralError
from croniter import croniter
from datetime import datetime
from datetime import timedelta
from logging import info
from firestore import DataError
from geocoder import GeocoderWrapper
from local_time import LocalTime


def rewrite_cron(self, cron, after, user):
    'Replaces references to sunrise and sunset in a cron expression.'
    if (('sunrise' not in cron) and ('sunset' not in cron)):
        return cron
    yesterday = (after - timedelta(days=1))
    midnight_cron = cron.replace('sunrise', '0 0').replace('sunset', '0 0')
    try:
        first_day = croniter(midnight_cron, yesterday).get_next(datetime)
        second_day = croniter(midnight_cron, first_day).get_next(datetime)
    except ValueError as e:
        raise DataError(e)
    zone = self._local_time.zone(user)
    try:
        home = self._astral[user.get('home')]
    except (AstralError, KeyError) as e:
        raise DataError(e)
    if ('sunrise' in cron):
        sunrises = map((lambda x: home.sunrise(x).astimezone(zone)), [first_day, second_day])
        next_sunrise = min(filter((lambda x: (x >= after)), sunrises))
        sunrise_cron = cron.replace('sunrise', ('%d %d' % (next_sunrise.minute, next_sunrise.hour)))
        info(('Rewrote cron: (%s) -> (%s), after %s' % (cron, sunrise_cron, after.strftime('%A %B %d %Y %H:%M:%S %Z'))))
        return sunrise_cron
    if ('sunset' in cron):
        sunsets = map((lambda x: home.sunset(x).astimezone(zone)), [first_day, second_day])
        next_sunset = min(filter((lambda x: (x >= after)), sunsets))
        sunset_cron = cron.replace('sunset', ('%d %d' % (next_sunset.minute, next_sunset.hour)))
        info(('Rewrote cron: (%s) -> (%s), after %s' % (cron, sunset_cron, after.strftime('%A %B %d %Y %H:%M:%S %Z'))))
        return sunset_cron
