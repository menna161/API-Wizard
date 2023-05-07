from django.contrib.sitemaps import Sitemap
from django.utils.timezone import datetime, get_default_timezone, make_aware
from articles.models import ArticleListPage, ArticlePage, ExternalArticleListPage, SeriesListPage, SeriesPage, Topic, TopicListPage
from core.models import HomePage
from events.models import EventListPage, EventPage
from jobs.models import JobPostingListPage, JobPostingPage
from newsletter.models import NewsletterListPage, NewsletterPage
from people.models import ContributorListPage, ContributorPage


def lastmod(self, obj):
    article = obj.articles.first()
    if article:
        return article.latest_revision_created_at
    else:
        return make_aware(datetime.min, get_default_timezone())
