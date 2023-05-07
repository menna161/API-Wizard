import sys
from datetime import datetime
from unittest import skipIf
from django.test import TestCase
from six import text_type
from django_fakery import factory
from django_fakery.compat import HAS_PSYCOPG2
from psycopg2.extras import DateTimeTZRange, NumericRange


def test_postgres_fields(self):
    gigis_special = factory.make('tests.SpecialtyPizza')
    self.assertTrue(isinstance(gigis_special.toppings, list))
    for topping in gigis_special.toppings:
        self.assertTrue(isinstance(topping, text_type))
    self.assertTrue(isinstance(gigis_special.metadata, dict))
    self.assertTrue(isinstance(gigis_special.price_range, NumericRange))
    self.assertTrue(isinstance(gigis_special.price_range.lower, int))
    self.assertTrue(isinstance(gigis_special.sales, NumericRange))
    self.assertTrue(isinstance(gigis_special.sales.lower, int))
    self.assertTrue(isinstance(gigis_special.available_on, DateTimeTZRange))
    self.assertTrue(isinstance(gigis_special.available_on.lower, datetime))
    self.assertNotEqual(gigis_special.available_on.lower.tzinfo, None)
    self.assertTrue(isinstance(gigis_special.nutritional_values, dict))
