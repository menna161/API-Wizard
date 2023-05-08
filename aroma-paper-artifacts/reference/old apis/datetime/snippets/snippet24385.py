import unittest
from clickhouse_driver.errors import ServerException, ErrorCodes
from airflow_clickhouse_plugin.hooks.clickhouse_hook import ClickHouseHook
from tests.integration.util import ClickHouseConnectionEnvVarTestCase
import pandas as pd
from clickhouse_driver import errors
from datetime import date
from clickhouse_driver import errors


def test_simple_insert_with_types_check(self):
    from datetime import date
    from clickhouse_driver import errors
    with self.assertRaises(errors.TypeMismatchError) as e:
        self._hook.run(f'INSERT INTO {self._temp_table_name} (test_field) VALUES', [(date(2012, 10, 25),)], types_check=True)
    self.assertIn('Expected UInt8', str(e.exception))
