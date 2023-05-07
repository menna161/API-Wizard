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


def test_blogpage_fallback_url(self):
    '\n        Testing how translated entries appear on a ``BlogPage`` that has no translation except for the default/fallback.\n        '
    page = BlogPage.objects.language('en').create(author=self.user, status=BlogPage.PUBLISHED, slug='blogpage')
    self.assertEqual(page.default_url, '/en/blogpage/')
    date = datetime(year=2016, month=5, day=1)
    entry = Entry.objects.language('en').create(author=self.user, slug='hello-en', publication_date=date)
    self.assertEqual(entry.default_url, '/en/blogpage/2016/05/hello-en/')
    with translation.override('nl'):
        entry.set_current_language('nl')
        self.assertEqual(entry.default_url, '/nl/blogpage/2016/05/hello-en/')
        entry.create_translation('nl', slug='hello-nl')
        self.assertEqual(entry.default_url, '/nl/blogpage/2016/05/hello-nl/')
