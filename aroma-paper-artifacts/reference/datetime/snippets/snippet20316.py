from abc import ABCMeta, abstractmethod
from contextlib import contextmanager
from datetime import datetime, timedelta
import logging
import os
import shutil
import tempfile
import unittest
import warnings
from click.testing import CliRunner
import agnostic
import agnostic.cli


def insert_migration(self, cursor, name, status, started=None, completed=None):
    ' Insert a row into the migration table. '
    logging.info('Inserting migration: %s [%s]', name, status)
    base_date = datetime(year=2016, month=1, day=1)
    if (started is None):
        offset = (timedelta(minutes=1) * self._migrations_inserted)
        started = (base_date + offset)
        self._migrations_inserted += 1
    if (completed is None):
        completed = (started + timedelta(seconds=59))
    query = 'INSERT INTO agnostic_migrations VALUES ({}, {}, {}, {})'.format(self._param, self._param, self._param, self._param)
    cursor.execute(query, (name, status, started, completed))
