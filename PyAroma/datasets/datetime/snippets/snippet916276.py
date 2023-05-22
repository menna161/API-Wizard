from __future__ import absolute_import, division, unicode_literals
import datetime
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, ObjectList, RichTextFieldPanel, TabbedInterface
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from themes.models import ThemeablePage


@property
def recent_contributors(self):
    endtime = timezone.now()
    starttime = (endtime - datetime.timedelta(days=365))
    contributors = ContributorPage.objects.live().filter(featured=False, article_links__article__isnull=False, article_links__isnull=False, article_links__article__first_published_at__range=[starttime, endtime]).order_by('last_name', 'first_name').distinct()
    return self.get_rows(contributors, number_of_columns=4)
