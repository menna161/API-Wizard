import unittest
from datetime import date, datetime
from decimal import Decimal
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Model
from django_mock_queries.query import MockModel, MockSet
from django_admin_search.utils import format_data


def test_model_choice_field_parse(self):
    qs = MockSet(MockModel(pk=0), MockModel(pk=1), MockModel(pk=2), model=ModelTest)
    field = forms.ModelChoiceField(queryset=qs)
    self.assertEqual(format_data(field, 0), 0)
    self.assertEqual(format_data(field, 1), 1)
    self.assertEqual(format_data(field, 2), 2)
    self.assertRaises(ValidationError, (lambda : format_data(field, 4)))
