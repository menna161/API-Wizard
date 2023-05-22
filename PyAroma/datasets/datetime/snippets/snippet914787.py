from django.core.management.base import BaseCommand, CommandError
from diary.models import Entry, Customer
from diary.views import get_today_now
import datetime


def add_arguments(self, parser):
    '\n        Define the date before when to delete entries either by\n        -a --age      age of the entry (from the date of the appointment)\n        -b --before   date before which to delete\n        '
    parser.add_argument('-a', '--age', help='age in years', type=int, default=0)
    parser.add_argument('-b', '--before', help='date HWM (yyyy-mm-dd)', type=datetime.date.fromisoformat, default=get_today_now()[0])
