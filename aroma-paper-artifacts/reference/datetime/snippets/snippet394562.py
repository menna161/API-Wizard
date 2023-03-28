import json
from datetime import datetime
from typing import List
import pytest
from fastapi.testclient import TestClient
from feast.feast_object import FeastObject
from feast.feature_server import get_app
from tests.integration.feature_repos.repo_configuration import construct_universal_feature_views
from tests.integration.feature_repos.universal.entities import customer, driver, location


@pytest.mark.integration
@pytest.mark.universal_online_stores
def test_push(python_fs_client):
    initial_temp = _get_temperatures_from_feature_server(python_fs_client, location_ids=[1])[0]
    json_data = json.dumps({'push_source_name': 'location_stats_push_source', 'df': {'location_id': [1], 'temperature': [(initial_temp * 100)], 'event_timestamp': [str(datetime.utcnow())], 'created': [str(datetime.utcnow())]}})
    response = python_fs_client.post('/push', data=json_data)
    assert (response.status_code == 200)
    assert (_get_temperatures_from_feature_server(python_fs_client, location_ids=[1]) == [(initial_temp * 100)])
