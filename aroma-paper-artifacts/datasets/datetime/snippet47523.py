import json
from collections import OrderedDict
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import SyndicationFeed, rfc3339_date, Rss201rev2Feed
from wagtail import VERSION as WAGTAIL_VERSION
from datetime import datetime, time
from django.utils.html import strip_tags
from django.apps import apps
from bs4 import BeautifulSoup
from .models import RSSFeedsSettings
from wagtail.core.models import Site
from wagtail.core.rich_text import expand_db_html
from wagtail.wagtailcore.models import Site
from wagtail.wagtailcore.rich_text import expand_db_html
from urlparse import urljoin
from urllib.parse import urljoin


def item_pubdate(self, item):
    if feed_item_date_field:
        if is_date_field_datetime:
            return getattr(item, feed_item_date_field)
        else:
            return datetime.combine(getattr(item, feed_item_date_field), time())
    else:
        return datetime.combine(item.date, time())
