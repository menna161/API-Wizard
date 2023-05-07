from django.test import TestCase
from django.utils import timezone
from faker import Faker
from django_fakery import shortcuts


def test_future_datetime(self):
    fn = shortcuts.future_datetime()
    date = fn(1, fake)
    self.assertTrue((date > timezone.now()))
    fn = shortcuts.future_datetime('+2d')
    date = fn(1, fake)
    self.assertTrue((date > timezone.now()))
