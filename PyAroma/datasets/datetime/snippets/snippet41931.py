from django.test import TestCase
from django.utils import timezone
from faker import Faker
from django_fakery import shortcuts


def test_past_datetime(self):
    fn = shortcuts.past_datetime()
    date = fn(1, fake)
    self.assertTrue((date < timezone.now()))
    fn = shortcuts.past_datetime('-2d')
    date = fn(1, fake)
    self.assertTrue((date < timezone.now()))
