import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
import pytest
from feast import FeatureView, Field
from feast.types import Float32, Int32
from tests.integration.feature_repos.repo_configuration import construct_universal_feature_views
from tests.integration.feature_repos.universal.entities import driver


@pytest.mark.integration
@pytest.mark.universal_offline_stores
def test_writing_incorrect_schema_fails(environment, universal_data_sources):
    'Tests that writing a dataframe with an incorrect schema fails.'
    store = environment.feature_store
    (_, _, data_sources) = universal_data_sources
    feature_views = construct_universal_feature_views(data_sources)
    driver_fv = feature_views.driver
    store.apply([driver(), driver_fv])
    now = datetime.utcnow()
    ts = pd.Timestamp(now).round('ms')
    expected_df = pd.DataFrame.from_dict({'event_timestamp': [(ts - timedelta(hours=3)), ts], 'driver_id': [1001, 1002], 'conv_rate': [random.random(), random.random()], 'incorrect_schema': [random.randint(0, 10), random.randint(0, 10)], 'created': [ts, ts]})
    with pytest.raises(ValueError):
        store.write_to_offline_store(driver_fv.name, expected_df, allow_registry_cache=False)
