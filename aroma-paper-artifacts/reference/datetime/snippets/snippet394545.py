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
def test_writing_consecutively_to_offline_store(environment, universal_data_sources):
    store = environment.feature_store
    (_, _, data_sources) = universal_data_sources
    driver_entity = driver()
    driver_stats = FeatureView(name='driver_stats', entities=[driver_entity], schema=[Field(name='avg_daily_trips', dtype=Int32), Field(name='conv_rate', dtype=Float32), Field(name='acc_rate', dtype=Float32)], source=data_sources.driver, ttl=timedelta(minutes=10))
    now = datetime.utcnow()
    ts = pd.Timestamp(now, unit='ns')
    entity_df = pd.DataFrame.from_dict({'driver_id': [1001, 1001], 'event_timestamp': [(ts + timedelta(hours=3)), (ts + timedelta(hours=4))]})
    store.apply([driver_entity, driver_stats])
    df = store.get_historical_features(entity_df=entity_df, features=['driver_stats:conv_rate', 'driver_stats:acc_rate', 'driver_stats:avg_daily_trips'], full_feature_names=False).to_df()
    assert df['conv_rate'].isnull().all()
    assert df['acc_rate'].isnull().all()
    assert df['avg_daily_trips'].isnull().all()
    first_df = pd.DataFrame.from_dict({'event_timestamp': [(ts + timedelta(hours=3)), (ts + timedelta(hours=4))], 'driver_id': [1001, 1001], 'conv_rate': [random.random(), random.random()], 'acc_rate': [random.random(), random.random()], 'avg_daily_trips': [random.randint(0, 10), random.randint(0, 10)], 'created': [ts, ts]})
    first_df = first_df.astype({'conv_rate': 'float32', 'acc_rate': 'float32'})
    store.write_to_offline_store(driver_stats.name, first_df, allow_registry_cache=False)
    after_write_df: pd.DataFrame = store.get_historical_features(entity_df=entity_df, features=['driver_stats:conv_rate', 'driver_stats:acc_rate', 'driver_stats:avg_daily_trips'], full_feature_names=False).to_df()
    after_write_df = after_write_df.sort_values('event_timestamp').reset_index(drop=True)
    print(f'''After: {after_write_df}
First: {first_df}''')
    print(f'''After: {after_write_df['conv_rate'].reset_index(drop=True)}
First: {first_df['conv_rate'].reset_index(drop=True)}''')
    assert (len(after_write_df) == len(first_df))
    for field in ['conv_rate', 'acc_rate', 'avg_daily_trips']:
        assert np.equal(after_write_df[field].reset_index(drop=True), first_df[field].reset_index(drop=True)).all(), f'''Field: {field}
After: {after_write_df[field].reset_index(drop=True)}
First: {first_df[field].reset_index(drop=True)}'''
    second_df = pd.DataFrame.from_dict({'event_timestamp': [(ts + timedelta(hours=5)), (ts + timedelta(hours=6))], 'driver_id': [1001, 1001], 'conv_rate': [random.random(), random.random()], 'acc_rate': [random.random(), random.random()], 'avg_daily_trips': [random.randint(0, 10), random.randint(0, 10)], 'created': [ts, ts]})
    second_df = second_df.astype({'conv_rate': 'float32', 'acc_rate': 'float32'})
    store.write_to_offline_store(driver_stats.name, second_df, allow_registry_cache=False)
    entity_df = pd.DataFrame.from_dict({'driver_id': [1001, 1001, 1001, 1001], 'event_timestamp': [(ts + timedelta(hours=3)), (ts + timedelta(hours=4)), (ts + timedelta(hours=5)), (ts + timedelta(hours=6))]})
    after_write_df = store.get_historical_features(entity_df=entity_df, features=['driver_stats:conv_rate', 'driver_stats:acc_rate', 'driver_stats:avg_daily_trips'], full_feature_names=False).to_df()
    after_write_df = after_write_df.sort_values('event_timestamp').reset_index(drop=True)
    expected_df = pd.concat([first_df, second_df])
    assert (len(after_write_df) == len(expected_df))
    for field in ['conv_rate', 'acc_rate', 'avg_daily_trips']:
        assert np.equal(after_write_df[field].reset_index(drop=True), expected_df[field].reset_index(drop=True)).all(), f'''Field: {field}
After: {after_write_df[field].reset_index(drop=True)}
First: {expected_df[field].reset_index(drop=True)}'''
