import copy
import itertools
import os
import warnings
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple, Union, cast
import pandas as pd
import pyarrow as pa
from colorama import Fore, Style
from google.protobuf.timestamp_pb2 import Timestamp
from tqdm import tqdm
from feast import feature_server, flags_helper, ui_server, utils
from feast.base_feature_view import BaseFeatureView
from feast.batch_feature_view import BatchFeatureView
from feast.data_source import DataSource, KafkaSource, KinesisSource, PushMode, PushSource
from feast.diff.infra_diff import InfraDiff, diff_infra_protos
from feast.diff.registry_diff import RegistryDiff, apply_diff_to_registry, diff_between
from feast.dqm.errors import ValidationFailed
from feast.entity import Entity
from feast.errors import DataSourceRepeatNamesException, EntityNotFoundException, FeatureNameCollisionError, FeatureViewNotFoundException, PushSourceNotFoundException, RequestDataNotFoundInEntityDfException, RequestDataNotFoundInEntityRowsException
from feast.feast_object import FeastObject
from feast.feature_service import FeatureService
from feast.feature_view import DUMMY_ENTITY, DUMMY_ENTITY_ID, DUMMY_ENTITY_NAME, DUMMY_ENTITY_VAL, FeatureView
from feast.inference import update_data_sources_with_inferred_event_timestamp_col, update_feature_views_with_inferred_features_and_entities
from feast.infra.infra_object import Infra
from feast.infra.provider import Provider, RetrievalJob, get_provider
from feast.infra.registry.base_registry import BaseRegistry
from feast.infra.registry.registry import Registry
from feast.infra.registry.sql import SqlRegistry
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.online_response import OnlineResponse
from feast.protos.feast.serving.ServingService_pb2 import FieldStatus, GetOnlineFeaturesResponse
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import RepeatedValue, Value
from feast.repo_config import RepoConfig, load_repo_config
from feast.repo_contents import RepoContents
from feast.request_feature_view import RequestFeatureView
from feast.saved_dataset import SavedDataset, SavedDatasetStorage, ValidationReference
from feast.stream_feature_view import StreamFeatureView
from feast.type_map import feast_value_type_to_python_type, python_values_to_proto_values
from feast.usage import log_exceptions, log_exceptions_and_usage, set_usage_attribute
from feast.value_type import ValueType
from feast.version import get_version
from feast.embedded_go.online_features_service import EmbeddedOnlineFeatureServer
from feast.data_source import PushSource
from feast.embedded_go.online_features_service import EmbeddedOnlineFeatureServer
from feast import transformation_server


@log_exceptions_and_usage
def get_historical_features(self, entity_df: Union[(pd.DataFrame, str)], features: Union[(List[str], FeatureService)], full_feature_names: bool=False) -> RetrievalJob:
    'Enrich an entity dataframe with historical feature values for either training or batch scoring.\n\n        This method joins historical feature data from one or more feature views to an entity dataframe by using a time\n        travel join.\n\n        Each feature view is joined to the entity dataframe using all entities configured for the respective feature\n        view. All configured entities must be available in the entity dataframe. Therefore, the entity dataframe must\n        contain all entities found in all feature views, but the individual feature views can have different entities.\n\n        Time travel is based on the configured TTL for each feature view. A shorter TTL will limit the\n        amount of scanning that will be done in order to find feature data for a specific entity key. Setting a short\n        TTL may result in null values being returned.\n\n        Args:\n            entity_df (Union[pd.DataFrame, str]): An entity dataframe is a collection of rows containing all entity\n                columns (e.g., customer_id, driver_id) on which features need to be joined, as well as a event_timestamp\n                column used to ensure point-in-time correctness. Either a Pandas DataFrame can be provided or a string\n                SQL query. The query must be of a format supported by the configured offline store (e.g., BigQuery)\n            features: The list of features that should be retrieved from the offline store. These features can be\n                specified either as a list of string feature references or as a feature service. String feature\n                references must have format "feature_view:feature", e.g. "customer_fv:daily_transactions".\n            full_feature_names: If True, feature names will be prefixed with the corresponding feature view name,\n                changing them from the format "feature" to "feature_view__feature" (e.g. "daily_transactions"\n                changes to "customer_fv__daily_transactions").\n\n        Returns:\n            RetrievalJob which can be used to materialize the results.\n\n        Raises:\n            ValueError: Both or neither of features and feature_refs are specified.\n\n        Examples:\n            Retrieve historical features from a local offline store.\n\n            >>> from feast import FeatureStore, RepoConfig\n            >>> import pandas as pd\n            >>> fs = FeatureStore(repo_path="project/feature_repo")\n            >>> entity_df = pd.DataFrame.from_dict(\n            ...     {\n            ...         "driver_id": [1001, 1002],\n            ...         "event_timestamp": [\n            ...             datetime(2021, 4, 12, 10, 59, 42),\n            ...             datetime(2021, 4, 12, 8, 12, 10),\n            ...         ],\n            ...     }\n            ... )\n            >>> retrieval_job = fs.get_historical_features(\n            ...     entity_df=entity_df,\n            ...     features=[\n            ...         "driver_hourly_stats:conv_rate",\n            ...         "driver_hourly_stats:acc_rate",\n            ...         "driver_hourly_stats:avg_daily_trips",\n            ...     ],\n            ... )\n            >>> feature_data = retrieval_job.to_df()\n        '
    _feature_refs = self._get_features(features)
    (all_feature_views, all_request_feature_views, all_on_demand_feature_views) = self._get_feature_views_to_use(features)
    if all_request_feature_views:
        warnings.warn('Request feature view is deprecated. Please use request data source instead', DeprecationWarning)
    (fvs, odfvs, request_fvs, request_fv_refs) = _group_feature_refs(_feature_refs, all_feature_views, all_request_feature_views, all_on_demand_feature_views)
    feature_views = list((view for (view, _) in fvs))
    on_demand_feature_views = list((view for (view, _) in odfvs))
    request_feature_views = list((view for (view, _) in request_fvs))
    set_usage_attribute('odfv', bool(on_demand_feature_views))
    set_usage_attribute('request_fv', bool(request_feature_views))
    if (type(entity_df) == pd.DataFrame):
        if self.config.coerce_tz_aware:
            entity_df = utils.make_df_tzaware(cast(pd.DataFrame, entity_df))
        for fv in request_feature_views:
            for feature in fv.features:
                if (feature.name not in entity_df.columns):
                    raise RequestDataNotFoundInEntityDfException(feature_name=feature.name, feature_view_name=fv.name)
        for odfv in on_demand_feature_views:
            odfv_request_data_schema = odfv.get_request_data_schema()
            for feature_name in odfv_request_data_schema.keys():
                if (feature_name not in entity_df.columns):
                    raise RequestDataNotFoundInEntityDfException(feature_name=feature_name, feature_view_name=odfv.name)
    _validate_feature_refs(_feature_refs, full_feature_names)
    _feature_refs = [ref for ref in _feature_refs if (ref not in request_fv_refs)]
    provider = self._get_provider()
    job = provider.get_historical_features(self.config, feature_views, _feature_refs, entity_df, self._registry, self.project, full_feature_names)
    return job
