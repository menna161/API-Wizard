import logging
import os
import shutil
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import agnostic
import agnostic.cli
from agnostic.mysql import MysqlBackend
from agnostic.postgres import PostgresBackend
from agnostic.sqlite import SqlLiteBackend


def test_invalid_migration_datetime(self):
    with self.assertRaises(ValueError):
        m = agnostic.Migration('1-my-name', 'bootstrapped', started_at=b'2018-01-01 12:00:00')
