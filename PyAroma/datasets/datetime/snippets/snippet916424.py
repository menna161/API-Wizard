from __future__ import unicode_literals
import argparse
import re
import six
from datetime import datetime
from django.core.management.base import BaseCommand
from analytics import utils
from articles.models import ArticlePage, SeriesPage


def _get_statistics_from_database(self, start_date, end_date):
    data_table = {}
    articles_of_interest = ArticlePage.objects.filter(first_published_at__range=[start_date, end_date])
    end_date_as_datetime = datetime.strptime(end_date, '%Y-%m-%d')
    for article in articles_of_interest:
        data_row = dict(title=article.title, url=article.url, published_date=article.first_published_at, days_published=self._calculate_days_published(article.first_published_at, end_date_as_datetime), parent_page=article.get_parent().title, category=article.category.name, is_video=article.video, is_interview=article.interview, is_visualization=article.visualization, word_count_by_type=self._calculate_word_count_by_type(article))
        assert (article.url not in data_table)
        data_table[article.url] = data_row
    series_of_interests = SeriesPage.objects.filter(first_published_at__range=[start_date, end_date])
    for series in series_of_interests:
        data_row = dict(title=series.title, url=series.url, published_date=series.first_published_at, days_published=self._calculate_days_published(series.first_published_at, end_date_as_datetime), parent_page=series.get_parent().title, category='', is_video=False, is_interview=False, is_visualization=False, word_count_by_type=self._calculate_word_count_by_type(series))
        assert (series.url not in data_table)
        data_table[series.url] = data_row
    return data_table
