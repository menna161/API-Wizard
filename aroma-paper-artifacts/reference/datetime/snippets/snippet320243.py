import json
import unittest
from unittest.mock import Mock, call, patch
from salesforce_bulk.util import IteratorBytesIO
import amaxa
from amaxa.api import Connection


def test_bulk_query_converts_datetimes(self):
    sf = Mock()
    sf.bulk_url = 'https://salesforce.com'
    conn = Connection(sf, '52.0')
    conn._bulk = Mock()
    retval = [{'Id': '001000000000001', 'CreatedDate': 1546659665000}, {'Id': '001000000000002', 'CreatedDate': None}]
    conn._bulk.is_batch_done = Mock(side_effect=[False, True])
    conn._bulk.create_query_job = Mock(return_value='075000000000000AAA')
    conn._bulk.get_all_results_for_query_batch = Mock(return_value=[IteratorBytesIO([json.dumps(retval).encode('utf-8')])])
    results = list(conn.bulk_api_query('Account', 'SELECT Id, CreatedDate, FROM Account', ['CreatedDate'], 5))
    self.assertEqual(results[0], {'Id': '001000000000001', 'CreatedDate': '2019-01-05T03:41:05.000+0000'})
    self.assertEqual(results[1], {'Id': '001000000000002', 'CreatedDate': None})
