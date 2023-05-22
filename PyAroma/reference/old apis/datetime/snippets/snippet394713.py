import subprocess
from datetime import datetime
import pandas as pd
from feast import FeatureStore
from feast.data_source import PushMode


def fetch_historical_features_entity_df(store: FeatureStore, for_batch_scoring: bool):
    entity_df = pd.DataFrame.from_dict({'driver_id': [1001, 1002, 1003], 'event_timestamp': [datetime(2021, 4, 12, 10, 59, 42), datetime(2021, 4, 12, 8, 12, 10), datetime(2021, 4, 12, 16, 40, 26)], 'label_driver_reported_satisfaction': [1, 5, 3], 'val_to_add': [1, 2, 3], 'val_to_add_2': [10, 20, 30]})
    if for_batch_scoring:
        entity_df['event_timestamp'] = pd.to_datetime('now', utc=True)
    training_df = store.get_historical_features(entity_df=entity_df, features=['driver_hourly_stats:conv_rate', 'driver_hourly_stats:acc_rate', 'driver_hourly_stats:avg_daily_trips', 'transformed_conv_rate:conv_rate_plus_val1', 'transformed_conv_rate:conv_rate_plus_val2']).to_df()
    print(training_df.head())
