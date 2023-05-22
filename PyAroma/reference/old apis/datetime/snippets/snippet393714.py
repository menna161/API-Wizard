from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from definitions import benchmark_feature_service, benchmark_feature_views, driver, driver_hourly_stats_view, entity, transformed_conv_rate
from feast import FeatureStore


def generate_data(num_rows: int, num_features: int, destination: str) -> pd.DataFrame:
    features = [f'feature_{i}' for i in range(num_features)]
    columns = (['entity', 'event_timestamp'] + features)
    df = pd.DataFrame(0, index=np.arange(num_rows), columns=columns)
    df['event_timestamp'] = datetime.utcnow()
    for column in features:
        df[column] = np.random.randint(1, num_rows, num_rows)
    df['entity'] = ('key-' + pd.Series(np.arange(1, (num_rows + 1))).astype(pd.StringDtype()))
    df.to_parquet(destination)
