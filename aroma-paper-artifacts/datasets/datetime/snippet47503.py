from django.test import TestCase
from django.apps import apps
from django.urls import reverse
from wagtail.core.rich_text import RichText
from wagtail.core.models import Collection, Page
from wagtail.images.tests.utils import Image, get_test_image_file
from wagtail_feeds.models import RSSFeedsSettings
from wagtail_feeds.feeds import BasicFeed, BasicJsonFeed, ExtendedFeed, ExtendedJsonFeed
from .models import HomePage, BlogPage, BlogStreamPage


def setUp(self):
    ContentType = apps.get_model('contenttypes.ContentType')
    Site = apps.get_model('wagtailcore.Site')
    Page.objects.get(id=2).delete()
    (homepage_content_type, created) = ContentType.objects.get_or_create(model='HomePage', app_label='tests')
    homepage = HomePage.objects.create(title='Homepage', slug='home', content_type=homepage_content_type, path='00010001', depth=1, url_path='/home-page')
    site = Site.objects.create(hostname='localhost', root_page=homepage, is_default_site=True)
    RSSFeedsSettings.objects.create(site=site, feed_app_label='tests', feed_model_name='BlogStreamPage', feed_title='Test Feed', feed_link='https://example.com', feed_description='Test Description', feed_item_description_field='intro', feed_item_content_field='body', feed_image_in_content=True, feed_item_date_field='date', is_feed_item_date_field_datetime=False)
    img_collection = Collection.objects.create(name='test', depth=1)
    image = Image.objects.create(title='Test image', file=get_test_image_file(), collection=img_collection)
    (blogpage_content_type, created) = ContentType.objects.get_or_create(model='BlogPage', app_label='tests')
    BlogPage.objects.create(title='BlogPage', intro='Welcome to Blog', body='This is the body of blog', date='2016-06-30', slug='blog-post', url_path='/home-page/blog-post/', content_type=blogpage_content_type, feed_image=image, path='000100010002', depth=2)
    (stream_blogpage_content_type, created) = ContentType.objects.get_or_create(model='BlogStreamPage', app_label='tests')
    stream_page = BlogStreamPage.objects.create(title='BlogStreamPage', intro='Welcome to Blog Stream Page', body=[('heading', 'foo'), ('paragraph', RichText((((((('<p>Rich text</p><div style="padding-bottom: 56.25%;"' + ' class="responsive-object"> <iframe width="480" height="270"') + ' src="https://www.youtube.com/embed/mSffkWuCkgQ?feature=oembed"') + ' frameborder="0" allowfullscreen=""></iframe>') + '<img alt="wagtail.jpg" height="500"') + ' src="/media/images/wagtail.original.jpg" width="1300">') + '</div>')))], date='2016-08-30', slug='blog-stream-post', url_path='/home-page/blog-stream-post/', content_type=stream_blogpage_content_type, feed_image=image, path='000100010003', depth=3)
