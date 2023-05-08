import os
import time
from datetime import datetime
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from feast import FeatureStore, RepoConfig
from feast.errors import FeatureViewNotFoundException
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import RegistryConfig
from tests.utils.cli_repo_creator import CliRunner, get_example_repo


def test_online_to_df():
    '\n    Test dataframe conversion. Make sure the response columns and rows are\n    the same order as the request.\n    '
    driver_ids = [1, 2, 3]
    customer_ids = [4, 5, 6]
    name = 'foo'
    lon_multiply = 1.0
    lat_multiply = 0.1
    age_multiply = 10
    avg_order_day_multiply = 1.0
    runner = CliRunner()
    with runner.local_repo(get_example_repo('example_feature_repo_1.py'), 'file') as store:
        driver_locations_fv = store.get_feature_view(name='driver_locations')
        customer_profile_fv = store.get_feature_view(name='customer_profile')
        customer_driver_combined_fv = store.get_feature_view(name='customer_driver_combined')
        provider = store._get_provider()
        for (d, c) in zip(driver_ids, customer_ids):
            '\n            driver table:\n                                    lon                    lat\n                1                   1.0                    0.1\n                2                   2.0                    0.2\n                3                   3.0                    0.3\n            '
            driver_key = EntityKeyProto(join_keys=['driver_id'], entity_values=[ValueProto(int64_val=d)])
            provider.online_write_batch(config=store.config, table=driver_locations_fv, data=[(driver_key, {'lat': ValueProto(double_val=(d * lat_multiply)), 'lon': ValueProto(string_val=str((d * lon_multiply)))}, datetime.utcnow(), datetime.utcnow())], progress=None)
            '\n            customer table\n            customer     avg_orders_day          name        age\n                4           4.0                  foo4         40\n                5           5.0                  foo5         50\n                6           6.0                  foo6         60\n            '
            customer_key = EntityKeyProto(join_keys=['customer_id'], entity_values=[ValueProto(string_val=str(c))])
            provider.online_write_batch(config=store.config, table=customer_profile_fv, data=[(customer_key, {'avg_orders_day': ValueProto(float_val=(c * avg_order_day_multiply)), 'name': ValueProto(string_val=(name + str(c))), 'age': ValueProto(int64_val=(c * age_multiply))}, datetime.utcnow(), datetime.utcnow())], progress=None)
            '\n            customer_driver_combined table\n            customer  driver    trips\n                4       1       4\n                5       2       10\n                6       3       18\n            '
            combo_keys = EntityKeyProto(join_keys=['customer_id', 'driver_id'], entity_values=[ValueProto(string_val=str(c)), ValueProto(int64_val=d)])
            provider.online_write_batch(config=store.config, table=customer_driver_combined_fv, data=[(combo_keys, {'trips': ValueProto(int64_val=(c * d))}, datetime.utcnow(), datetime.utcnow())], progress=None)
        result_df = store.get_online_features(features=['driver_locations:lon', 'driver_locations:lat', 'customer_profile:avg_orders_day', 'customer_profile:name', 'customer_profile:age', 'customer_driver_combined:trips'], entity_rows=[{'driver_id': d, 'customer_id': c} for (d, c) in zip(reversed(driver_ids), reversed(customer_ids))]).to_df()
        '\n        Construct the expected dataframe with reversed row order like so:\n        driver  customer     lon    lat     avg_orders_day      name        age     trips\n            3       6        3.0    0.3         6.0             foo6        60       18\n            2       5        2.0    0.2         5.0             foo5        50       10\n            1       4        1.0    0.1         4.0             foo4        40       4\n        '
        df_dict = {'driver_id': driver_ids, 'customer_id': [str(c) for c in customer_ids], 'lon': [str((d * lon_multiply)) for d in driver_ids], 'lat': [(d * lat_multiply) for d in driver_ids], 'avg_orders_day': [(c * avg_order_day_multiply) for c in customer_ids], 'name': [(name + str(c)) for c in customer_ids], 'age': [(c * age_multiply) for c in customer_ids], 'trips': [(d * c) for (d, c) in zip(driver_ids, customer_ids)]}
        ordered_column = ['driver_id', 'customer_id', 'lon', 'lat', 'avg_orders_day', 'name', 'age', 'trips']
        expected_df = pd.DataFrame({k: reversed(v) for (k, v) in df_dict.items()})
        assert_frame_equal(result_df[ordered_column], expected_df)