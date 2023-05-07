from datetime import timedelta
from defusedxml.lxml import fromstring
from lxml import etree
import json
from django import template


@register.filter
def datetimerange_as_pretty_delta(value):
    if value:
        return pretty_timedelta((value.upper - value.lower))
