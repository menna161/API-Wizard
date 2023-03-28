from datetime import datetime, timedelta, tzinfo
from bisect import bisect_right
import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError
from sets import Set as set


def localize(self, dt, is_dst=False):
    "Convert naive time to local time.\n\n        This method should be used to construct localtimes, rather\n        than passing a tzinfo argument to a datetime constructor.\n\n        is_dst is used to determine the correct timezone in the ambigous\n        period at the end of daylight saving time.\n\n        >>> from pytz import timezone\n        >>> fmt = '%Y-%m-%d %H:%M:%S %Z (%z)'\n        >>> amdam = timezone('Europe/Amsterdam')\n        >>> dt  = datetime(2004, 10, 31, 2, 0, 0)\n        >>> loc_dt1 = amdam.localize(dt, is_dst=True)\n        >>> loc_dt2 = amdam.localize(dt, is_dst=False)\n        >>> loc_dt1.strftime(fmt)\n        '2004-10-31 02:00:00 CEST (+0200)'\n        >>> loc_dt2.strftime(fmt)\n        '2004-10-31 02:00:00 CET (+0100)'\n        >>> str(loc_dt2 - loc_dt1)\n        '1:00:00'\n\n        Use is_dst=None to raise an AmbiguousTimeError for ambiguous\n        times at the end of daylight saving time\n\n        >>> try:\n        ...     loc_dt1 = amdam.localize(dt, is_dst=None)\n        ... except AmbiguousTimeError:\n        ...     print('Ambiguous')\n        Ambiguous\n\n        is_dst defaults to False\n\n        >>> amdam.localize(dt) == amdam.localize(dt, False)\n        True\n\n        is_dst is also used to determine the correct timezone in the\n        wallclock times jumped over at the start of daylight saving time.\n\n        >>> pacific = timezone('US/Pacific')\n        >>> dt = datetime(2008, 3, 9, 2, 0, 0)\n        >>> ploc_dt1 = pacific.localize(dt, is_dst=True)\n        >>> ploc_dt2 = pacific.localize(dt, is_dst=False)\n        >>> ploc_dt1.strftime(fmt)\n        '2008-03-09 02:00:00 PDT (-0700)'\n        >>> ploc_dt2.strftime(fmt)\n        '2008-03-09 02:00:00 PST (-0800)'\n        >>> str(ploc_dt2 - ploc_dt1)\n        '1:00:00'\n\n        Use is_dst=None to raise a NonExistentTimeError for these skipped\n        times.\n\n        >>> try:\n        ...     loc_dt1 = pacific.localize(dt, is_dst=None)\n        ... except NonExistentTimeError:\n        ...     print('Non-existent')\n        Non-existent\n        "
    if (dt.tzinfo is not None):
        raise ValueError('Not naive datetime (tzinfo is already set)')
    possible_loc_dt = set()
    for delta in [timedelta(days=(- 1)), timedelta(days=1)]:
        loc_dt = (dt + delta)
        idx = max(0, (bisect_right(self._utc_transition_times, loc_dt) - 1))
        inf = self._transition_info[idx]
        tzinfo = self._tzinfos[inf]
        loc_dt = tzinfo.normalize(dt.replace(tzinfo=tzinfo))
        if (loc_dt.replace(tzinfo=None) == dt):
            possible_loc_dt.add(loc_dt)
    if (len(possible_loc_dt) == 1):
        return possible_loc_dt.pop()
    if (len(possible_loc_dt) == 0):
        if (is_dst is None):
            raise NonExistentTimeError(dt)
        elif is_dst:
            return (self.localize((dt + timedelta(hours=6)), is_dst=True) - timedelta(hours=6))
        else:
            return (self.localize((dt - timedelta(hours=6)), is_dst=False) + timedelta(hours=6))
    if (is_dst is None):
        raise AmbiguousTimeError(dt)
    filtered_possible_loc_dt = [p for p in possible_loc_dt if (bool(p.tzinfo._dst) == is_dst)]
    if (len(filtered_possible_loc_dt) == 1):
        return filtered_possible_loc_dt[0]
    if (len(filtered_possible_loc_dt) == 0):
        filtered_possible_loc_dt = list(possible_loc_dt)
    dates = {}
    for local_dt in filtered_possible_loc_dt:
        utc_time = (local_dt.replace(tzinfo=None) - local_dt.tzinfo._utcoffset)
        assert (utc_time not in dates)
        dates[utc_time] = local_dt
    return dates[[min, max][(not is_dst)](dates)]
