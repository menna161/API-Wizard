from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals
import os
import io
import json
import uuid
import pytest
import datetime
import tableschema
from copy import deepcopy
from decimal import Decimal
from tabulator import Stream
from apiclient.discovery import build
from oauth2client.client import GoogleCredentials
from tableschema_bigquery import Storage


def test_storage():
    storage = Storage(SERVICE, project=PROJECT, dataset=DATASET, prefix=PREFIX)
    storage.delete()
    storage.create(['articles', 'comments'], [ARTICLES['schema'], COMMENTS['schema']])
    storage.create('temporal', TEMPORAL['schema'])
    storage.create('location', LOCATION['schema'])
    storage.create('compound', COMPOUND['schema'])
    storage.write('articles', ARTICLES['data'])
    storage.write('comments', COMMENTS['data'])
    storage.write('temporal', TEMPORAL['data'])
    storage.write('location', LOCATION['data'])
    storage.write('compound', COMPOUND['data'])
    storage = Storage(SERVICE, project=PROJECT, dataset=DATASET, prefix=PREFIX)
    assert (storage.buckets == ['articles', 'comments', 'compound', 'location', 'temporal'])
    assert (storage.describe('articles') == ARTICLES['schema'])
    assert (storage.describe('comments') == {'fields': [{'name': 'entry_id', 'type': 'integer', 'constraints': {'required': True}}, {'name': 'comment', 'type': 'string'}, {'name': 'note', 'type': 'string'}]})
    assert (storage.describe('temporal') == {'fields': [{'name': 'date', 'type': 'date'}, {'name': 'date_year', 'type': 'date'}, {'name': 'datetime', 'type': 'datetime'}, {'name': 'duration', 'type': 'string'}, {'name': 'time', 'type': 'time'}, {'name': 'year', 'type': 'integer'}, {'name': 'yearmonth', 'type': 'string'}]})
    assert (storage.describe('location') == {'fields': [{'name': 'location', 'type': 'string'}, {'name': 'geopoint', 'type': 'string'}]})
    assert (storage.describe('compound') == {'fields': [{'name': 'stats', 'type': 'string'}, {'name': 'persons', 'type': 'string'}]})
    assert (storage.read('articles') == cast(ARTICLES)['data'])
    assert (storage.read('comments') == cast(COMMENTS)['data'])
    assert (storage.read('temporal') == cast(TEMPORAL, skip=['duration', 'yearmonth'])['data'])
    assert (storage.read('location') == cast(LOCATION, skip=['geojson', 'geopoint'])['data'])
    assert (storage.read('compound') == cast(COMPOUND, skip=['array', 'object'])['data'])
    storage.describe('compound', COMPOUND['schema'])
    assert (storage.read('compound') == cast(COMPOUND)['data'])
    with pytest.raises(tableschema.exceptions.StorageError):
        storage.delete('non_existent')
    storage.delete()
