import logging
import requests
from .utils import make_enum


def add_event(self, name, start_date, end_date=None, all_day=None, description=None, category_id=None, event_id=None):
    'Add event for a given date range.\n\n        Args:\n          name: Name of event\n          start_date: Start datetimestamp (epoch time)\n          end_date: End datetimestamp (epoch time)\n          all_day: boolean\n          description: description of event (default none)\n          category id: which calendar your event is on (defaults to primary)\n          event id: series id\n\n        Returns:\n          JSON response.'
    params = []
    if name:
        params.append(('name=%s' % name))
    if start_date:
        params.append(('starts_on=%s' % start_date))
    if end_date:
        params.append(('ends_on=%s' % end_date))
    if all_day:
        params.append(('all_day=%s' % all_day))
    if description:
        params.append(('description=%s' % description))
    if category_id:
        params.append(('category_id=%s' % category_id))
    if event_id:
        params.append(('event_id=%s' % event_id))
    return self._request(('%s/add?%s' % (ENDPOINTS.EVENTS, '&'.join(params))))
