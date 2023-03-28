from datetime import datetime
import pandas as pd
import pytest
from feast import Field
from feast.errors import SpecifiedFeaturesNotPresentError
from feast.infra.offline_stores.file_source import FileSource
from feast.types import Float64
from tests.integration.feature_repos.universal.entities import customer, driver, item
from tests.integration.feature_repos.universal.feature_views import conv_rate_plus_100_feature_view, create_conv_rate_request_source, create_driver_hourly_stats_batch_feature_view, create_item_embeddings_batch_feature_view, create_similarity_request_source, similarity_feature_view


@pytest.mark.integration
@pytest.mark.parametrize('infer_features', [True, False], ids=(lambda v: str(v)))
def test_infer_odfv_list_features(environment, infer_features, tmp_path):
    fake_embedding = [1.0, 1.0]
    items_df = pd.DataFrame(data={'item_id': [0], 'embedding_float': [fake_embedding], 'embedding_double': [fake_embedding], 'event_timestamp': [pd.Timestamp(datetime.utcnow())], 'created': [pd.Timestamp(datetime.utcnow())]})
    output_path = f'{tmp_path}/items.parquet'
    items_df.to_parquet(output_path)
    fake_items_src = FileSource(path=output_path, timestamp_field='event_timestamp', created_timestamp_column='created')
    item_feature_view = create_item_embeddings_batch_feature_view(fake_items_src)
    sim_odfv = similarity_feature_view([item_feature_view, create_similarity_request_source()], infer_features=infer_features)
    store = environment.feature_store
    store.apply([item(), item_feature_view, sim_odfv])
    odfv = store.get_on_demand_feature_view('similarity')
    assert (len(odfv.features) == 2)
