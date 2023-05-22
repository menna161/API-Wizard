import random
import dataclasses
import json
from dataclasses import dataclass
from datetime import datetime
import random
from decimal import Decimal
from traceback import print_tb
import unittest
from django.test import TestCase
from django.contrib.auth.models import User
import factory
from faker import Faker
from djaq import DjaqQuery as DQ
from django.db.models import Count, Q
from django.db.models import DecimalField, Avg, Max
from books.models import GENRE_CHOICES
from books.models import Author, Publisher, Book, Store, Profile, Consortium


def get_random_genre():
    return GENRE_CHOICES[random.randint(0, (len(GENRE_CHOICES) - 1))][0]
