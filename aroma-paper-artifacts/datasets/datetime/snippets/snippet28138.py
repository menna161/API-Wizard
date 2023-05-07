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


def test_remove_old_succeeded_job_logs(self):
    mock_date = datetime.datetime(2022, 5, 1, 12, 0, 0)
    for _ in range(5):
        with freeze_time(mock_date):
            call_command('runcrons', self.run_and_remove_old_logs)
        self.assertEqual(CronJobLog.objects.all().count(), 1)
        self.assertEqual(CronJobLog.objects.all().first().end_time, mock_date)
