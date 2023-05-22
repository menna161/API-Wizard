import subprocess
from datetime import datetime
import pandas as pd
from feast import FeatureStore
from feast.data_source import PushMode


def run_demo():
    store = FeatureStore(repo_path='.')
    print('\n--- Run feast apply to setup feature store on Postgres ---')
    subprocess.run(['feast', 'apply'])
    print('\n--- Historical features for training ---')
    fetch_historical_features_entity_df(store, for_batch_scoring=False)
    print('\n--- Historical features for batch scoring ---')
    fetch_historical_features_entity_df(store, for_batch_scoring=True)
    print('\n--- Load features into online store ---')
    store.materialize_incremental(end_date=datetime.now())
    print('\n--- Online features ---')
    fetch_online_features(store)
    print('\n--- Online features retrieved (instead) through a feature service---')
    fetch_online_features(store, source='feature_service')
    print('\n--- Online features retrieved (using feature service v3, which uses a feature view with a push source---')
    fetch_online_features(store, source='push')
    print('\n--- Simulate a stream event ingestion of the hourly stats df ---')
    event_df = pd.DataFrame.from_dict({'driver_id': [1001], 'event_timestamp': [datetime.now()], 'created': [datetime.now()], 'conv_rate': [1.0], 'acc_rate': [1.0], 'avg_daily_trips': [1000]})
    print(event_df)
    store.push('driver_stats_push_source', event_df, to=PushMode.ONLINE_AND_OFFLINE)
    print('\n--- Online features again with updated values from a stream push---')
    fetch_online_features(store, source='push')
    print('\n--- Run feast teardown ---')
    subprocess.run(['feast', 'teardown'])
