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


def test_online() -> None:
    '\n    Test reading from the online store in local mode.\n    '
    runner = CliRunner()
    with runner.local_repo(get_example_repo('example_feature_repo_1.py'), 'file') as store:
        driver_locations_fv = store.get_feature_view(name='driver_locations')
        customer_profile_fv = store.get_feature_view(name='customer_profile')
        customer_driver_combined_fv = store.get_feature_view(name='customer_driver_combined')
        provider = store._get_provider()
        driver_key = EntityKeyProto(join_keys=['driver_id'], entity_values=[ValueProto(int64_val=1)])
        provider.online_write_batch(config=store.config, table=driver_locations_fv, data=[(driver_key, {'lat': ValueProto(double_val=0.1), 'lon': ValueProto(string_val='1.0')}, datetime.utcnow(), datetime.utcnow())], progress=None)
        customer_key = EntityKeyProto(join_keys=['customer_id'], entity_values=[ValueProto(string_val='5')])
        provider.online_write_batch(config=store.config, table=customer_profile_fv, data=[(customer_key, {'avg_orders_day': ValueProto(float_val=1.0), 'name': ValueProto(string_val='John'), 'age': ValueProto(int64_val=3)}, datetime.utcnow(), datetime.utcnow())], progress=None)
        customer_key = EntityKeyProto(join_keys=['customer_id', 'driver_id'], entity_values=[ValueProto(string_val='5'), ValueProto(int64_val=1)])
        provider.online_write_batch(config=store.config, table=customer_driver_combined_fv, data=[(customer_key, {'trips': ValueProto(int64_val=7)}, datetime.utcnow(), datetime.utcnow())], progress=None)
        result = store.get_online_features(features=['driver_locations:lon', 'customer_profile:avg_orders_day', 'customer_profile:name', 'customer_driver_combined:trips'], entity_rows=[{'driver_id': 1, 'customer_id': '5'}, {'driver_id': 1, 'customer_id': 5}], full_feature_names=False).to_dict()
        assert ('lon' in result)
        assert ('avg_orders_day' in result)
        assert ('name' in result)
        assert (result['driver_id'] == [1, 1])
        assert (result['customer_id'] == ['5', '5'])
        assert (result['lon'] == ['1.0', '1.0'])
        assert (result['avg_orders_day'] == [1.0, 1.0])
        assert (result['name'] == ['John', 'John'])
        assert (result['trips'] == [7, 7])
        result = store.get_online_features(features=['customer_driver_combined:trips'], entity_rows=[{'driver_id': 0, 'customer_id': 0}], full_feature_names=False).to_dict()
        assert ('trips' in result)
        with pytest.raises(FeatureViewNotFoundException):
            store.get_online_features(features=['driver_locations_bad:lon'], entity_rows=[{'driver_id': 1}], full_feature_names=False)
        cache_ttl = 1
        fs_fast_ttl = FeatureStore(config=RepoConfig(registry=RegistryConfig(path=store.config.registry, cache_ttl_seconds=cache_ttl), online_store=store.config.online_store, project=store.project, provider=store.config.provider, entity_key_serialization_version=2))
        result = fs_fast_ttl.get_online_features(features=['driver_locations:lon', 'customer_profile:avg_orders_day', 'customer_profile:name', 'customer_driver_combined:trips'], entity_rows=[{'driver_id': 1, 'customer_id': 5}], full_feature_names=False).to_dict()
        assert (result['lon'] == ['1.0'])
        assert (result['trips'] == [7])
        os.rename(store.config.registry, (store.config.registry + '_fake'))
        time.sleep(cache_ttl)
        with pytest.raises(FileNotFoundError):
            fs_fast_ttl.get_online_features(features=['driver_locations:lon', 'customer_profile:avg_orders_day', 'customer_profile:name', 'customer_driver_combined:trips'], entity_rows=[{'driver_id': 1, 'customer_id': 5}], full_feature_names=False).to_dict()
        os.rename((store.config.registry + '_fake'), store.config.registry)
        result = fs_fast_ttl.get_online_features(features=['driver_locations:lon', 'customer_profile:avg_orders_day', 'customer_profile:name', 'customer_driver_combined:trips'], entity_rows=[{'driver_id': 1, 'customer_id': 5}], full_feature_names=False).to_dict()
        assert (result['lon'] == ['1.0'])
        assert (result['trips'] == [7])
        fs_infinite_ttl = FeatureStore(config=RepoConfig(registry=RegistryConfig(path=store.config.registry, cache_ttl_seconds=0), online_store=store.config.online_store, project=store.project, provider=store.config.provider, entity_key_serialization_version=2))
        result = fs_infinite_ttl.get_online_features(features=['driver_locations:lon', 'customer_profile:avg_orders_day', 'customer_profile:name', 'customer_driver_combined:trips'], entity_rows=[{'driver_id': 1, 'customer_id': 5}], full_feature_names=False).to_dict()
        assert (result['lon'] == ['1.0'])
        assert (result['trips'] == [7])
        time.sleep(2)
        os.rename(store.config.registry, (store.config.registry + '_fake'))
        result = fs_infinite_ttl.get_online_features(features=['driver_locations:lon', 'customer_profile:avg_orders_day', 'customer_profile:name', 'customer_driver_combined:trips'], entity_rows=[{'driver_id': 1, 'customer_id': 5}], full_feature_names=False).to_dict()
        assert (result['lon'] == ['1.0'])
        assert (result['trips'] == [7])
        with pytest.raises(FileNotFoundError):
            fs_infinite_ttl.refresh_registry()
        os.rename((store.config.registry + '_fake'), store.config.registry)
