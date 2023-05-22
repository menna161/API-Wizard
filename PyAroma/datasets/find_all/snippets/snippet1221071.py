import unittest
import datetime as dt
import sqlite3
import forest.db.database


def test_find_all_available_dates(self):
    self.cursor.executemany('\n            INSERT INTO time (i, value) VALUES(:i, :value)\n        ', [dict(i=0, value='2018-01-01T00:00:00'), dict(i=1, value='2018-01-01T01:00:00')])
    result = self.database.fetch_dates(pattern='a*.nc')
    expect = ['2018-01-01T00:00:00', '2018-01-01T01:00:00']
    self.assertEqual(expect, result)
