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
def test_reorder_columns(environment, universal_data_sources):
    'Tests that a dataframe with columns in the wrong order is reordered.'
    store = environment.feature_store
    (_, _, data_sources) = universal_data_sources
    feature_views = construct_universal_feature_views(data_sources)
    driver_fv = feature_views.driver
    store.apply([driver(), driver_fv])
    now = datetime.utcnow()
    ts = pd.Timestamp(now).round('ms')
    df_to_write = pd.DataFrame.from_dict({'avg_daily_trips': [random.randint(0, 10), random.randint(0, 10)], 'created': [ts, ts], 'conv_rate': [random.random(), random.random()], 'event_timestamp': [ts, ts], 'acc_rate': [random.random(), random.random()], 'driver_id': [1001, 1001]})
    store.write_to_offline_store(driver_fv.name, df_to_write, allow_registry_cache=False)
