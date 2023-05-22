from datetime import date, datetime
from django.conf import settings
from django.template import Library
from tag_parser.basetags import BaseAssignmentOrInclusionNode, BaseAssignmentOrOutputNode
from fluent_blogs.models import get_entry_model
from fluent_blogs.models.query import query_entries, query_tags
from fluent_blogs.pagetypes.blogpage.models import BlogPage
from fluent_pages.templatetags.appurl_tags import appurl
from django.template.defaulttags import url


@register.filter
def format_year(year):
    '\n    Format the year value of the ``YearArchiveView``,\n    which can be a integer or date object.\n\n    This tag is no longer needed, but exists for template compatibility.\n    It was a compatibility tag for Django 1.4.\n    '
    if isinstance(year, (date, datetime)):
        return unicode(year.year)
    else:
        return unicode(year)
