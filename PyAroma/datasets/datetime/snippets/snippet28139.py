import datetime
import threading
from time import sleep
from datetime import timedelta
from unittest import skip
from mock import patch
from freezegun import freeze_time
from django import db
from django.test import TransactionTestCase
from django.core.management import call_command
from django.test.utils import override_settings
from django.test.client import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django_cron.helpers import humanize_duration
from django_cron.models import CronJobLog, CronJobLock
import test_crons


def test_run_job_with_logs_in_future(self):
    mock_date_in_future = datetime.datetime(2222, 5, 1, 12, 0, 0)
    with freeze_time(mock_date_in_future):
        call_command('runcrons', self.five_mins_cron)
        self.assertEqual(CronJobLog.objects.all().count(), 1)
        self.assertEqual(CronJobLog.objects.all().first().end_time, mock_date_in_future)
    mock_date_in_past = (mock_date_in_future - timedelta(days=1000))
    with freeze_time(mock_date_in_past):
        call_command('runcrons', self.five_mins_cron)
        self.assertEqual(CronJobLog.objects.all().count(), 2)
        self.assertEqual(CronJobLog.objects.all().earliest('start_time').end_time, mock_date_in_past)
    mock_date_in_past_plus_one_min = (mock_date_in_future + timedelta(minutes=1))
    with freeze_time(mock_date_in_past_plus_one_min):
        call_command('runcrons', self.five_mins_cron)
        self.assertEqual(CronJobLog.objects.all().count(), 2)
        self.assertEqual(CronJobLog.objects.all().earliest('start_time').end_time, mock_date_in_past)
