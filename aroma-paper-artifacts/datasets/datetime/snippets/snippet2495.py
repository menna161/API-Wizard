from datetime import datetime
from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.test import RequestFactory, TestCase
from django.test.utils import override_settings
from django.urls import reverse
from django.utils import translation
from fluent_pages.urlresolvers import PageTypeNotMounted
from fluent_blogs.admin import EntryAdmin
from fluent_blogs.models import Entry
from fluent_blogs.pagetypes.blogpage.models import BlogPage


def test_no_blogpage(self):
    '\n        When there is no blog page, the system should detect this.\n        '
    date = datetime(year=2016, month=5, day=1)
    entry = Entry.objects.language('en').create(author=self.user, slug='foo', publication_date=date)
    self.assertRaises(PageTypeNotMounted, (lambda : entry.default_url))
    self.assertEqual(entry.get_absolute_url_format(), '/.../2016/05/{slug}/')
