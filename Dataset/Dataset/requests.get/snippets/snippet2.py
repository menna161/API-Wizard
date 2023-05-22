from __future__ import print_function
import re
import warnings
import requests
import tweepy


def get_first_timer_issues():
    'Fetches the first page of issues with the label first-timers-label which are still open.'
    items = []
    for query in queries:
        res = requests.get(query)
        if (res.status_code == 403):
            warnings.warn('Rate limit reached')
            return items
        elif res.ok:
            items.extend(res.json()['items'])
        else:
            raise RuntimeError((('Could not handle response: ' + str(res)) + ' from the API.'))
    return items
