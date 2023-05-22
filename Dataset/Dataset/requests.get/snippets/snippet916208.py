import logging
import os
import re
from datetime import timedelta
import requests
import six
from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from six.moves.urllib.parse import urlparse, urlunparse


def _get_facebook_count(self):
    '\n        Get the latest Facebook Share Count from https://graph.facebook.com\n\n        Content:\n            example_json_response = {\n               "https://opencanada.org/features/five-issues-should-decide-future-internet/": {\n                  "og_object": {\n                     "id": "1330184950343806",\n                     "description": "With a new report on online governance out, we look at the\nconsiderations...\n                     "title": "Five issues that should decide the future of the Internet",\n                     "type": "article",\n                     "updated_time": "2016-08-23T03:20:45+0000"\n                  },\n                  "share": {\n                     "comment_count": 0,\n                     "share_count": 87\n                  },\n                  "id": "https://opencanada.org/features/five-issues-should-decide-future-internet/"\n               },\n               "http://opencanada.org/features/five-issues-should-decide-future-internet/": {\n                  "og_object": {\n                     "id": "1330184950343806",\n                     "description": "With a new report on online governance out, we look at the\nconsiderations...\n                     "title": "Five issues that should decide the future of the Internet",\n                     "type": "article",\n                     "updated_time": "2016-08-23T03:20:45+0000"\n                  },\n                  "share": {\n                     "comment_count": 0,\n                     "share_count": 87\n                  },\n                  "id": "http://opencanada.org/features/five-issues-should-decide-future-internet/"\n               }\n            }\n        '
    url = 'https://graph.facebook.com/?ids=https://opencanada.org{0},http://opencanada.org{0}'.format(self.url)
    total_shares = 0
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException:
        logger.error('There was an error getting the Facebook share count.', exc_info=True, extra={'page': self})
        return total_shares
    try:
        json_response = response.json()
    except ValueError:
        logger.error('There was an error decoding the JSON from the request to Facebook.', exc_info=True, extra={'page': self})
        return total_shares
    for (key, values) in six.iteritems(json_response):
        share_json = values.get('share', {})
        facebook_share_count = share_json.get('share_count', 0)
        if (facebook_share_count > total_shares):
            total_shares = facebook_share_count
    return total_shares
