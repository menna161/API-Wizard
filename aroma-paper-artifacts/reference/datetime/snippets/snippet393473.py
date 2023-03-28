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
def apply(self, objects: Union[(DataSource, Entity, FeatureView, OnDemandFeatureView, RequestFeatureView, BatchFeatureView, StreamFeatureView, FeatureService, ValidationReference, List[FeastObject])], objects_to_delete: Optional[List[FeastObject]]=None, partial: bool=True):
    'Register objects to metadata store and update related infrastructure.\n\n        The apply method registers one or more definitions (e.g., Entity, FeatureView) and registers or updates these\n        objects in the Feast registry. Once the apply method has updated the infrastructure (e.g., create tables in\n        an online store), it will commit the updated registry. All operations are idempotent, meaning they can safely\n        be rerun.\n\n        Args:\n            objects: A single object, or a list of objects that should be registered with the Feature Store.\n            objects_to_delete: A list of objects to be deleted from the registry and removed from the\n                provider\'s infrastructure. This deletion will only be performed if partial is set to False.\n            partial: If True, apply will only handle the specified objects; if False, apply will also delete\n                all the objects in objects_to_delete, and tear down any associated cloud resources.\n\n        Raises:\n            ValueError: The \'objects\' parameter could not be parsed properly.\n\n        Examples:\n            Register an Entity and a FeatureView.\n\n            >>> from feast import FeatureStore, Entity, FeatureView, Feature, FileSource, RepoConfig\n            >>> from datetime import timedelta\n            >>> fs = FeatureStore(repo_path="project/feature_repo")\n            >>> driver = Entity(name="driver_id", description="driver id")\n            >>> driver_hourly_stats = FileSource(\n            ...     path="project/feature_repo/data/driver_stats.parquet",\n            ...     timestamp_field="event_timestamp",\n            ...     created_timestamp_column="created",\n            ... )\n            >>> driver_hourly_stats_view = FeatureView(\n            ...     name="driver_hourly_stats",\n            ...     entities=[driver],\n            ...     ttl=timedelta(seconds=86400 * 1),\n            ...     source=driver_hourly_stats,\n            ... )\n            >>> fs.apply([driver_hourly_stats_view, driver]) # register entity and feature view\n        '
    if (not isinstance(objects, Iterable)):
        objects = [objects]
    assert isinstance(objects, list)
    if (not objects_to_delete):
        objects_to_delete = []
    entities_to_update = [ob for ob in objects if isinstance(ob, Entity)]
    views_to_update = [ob for ob in objects if ((isinstance(ob, FeatureView) or isinstance(ob, BatchFeatureView)) and (not isinstance(ob, StreamFeatureView)))]
    sfvs_to_update = [ob for ob in objects if isinstance(ob, StreamFeatureView)]
    request_views_to_update = [ob for ob in objects if isinstance(ob, RequestFeatureView)]
    odfvs_to_update = [ob for ob in objects if isinstance(ob, OnDemandFeatureView)]
    services_to_update = [ob for ob in objects if isinstance(ob, FeatureService)]
    data_sources_set_to_update = {ob for ob in objects if isinstance(ob, DataSource)}
    validation_references_to_update = [ob for ob in objects if isinstance(ob, ValidationReference)]
    batch_sources_to_add: List[DataSource] = []
    for data_source in data_sources_set_to_update:
        if (isinstance(data_source, PushSource) or isinstance(data_source, KafkaSource) or isinstance(data_source, KinesisSource)):
            assert data_source.batch_source
            batch_sources_to_add.append(data_source.batch_source)
    for batch_source in batch_sources_to_add:
        data_sources_set_to_update.add(batch_source)
    for fv in itertools.chain(views_to_update, sfvs_to_update):
        data_sources_set_to_update.add(fv.batch_source)
        if fv.stream_source:
            data_sources_set_to_update.add(fv.stream_source)
    if request_views_to_update:
        warnings.warn('Request feature view is deprecated. Please use request data source instead', DeprecationWarning)
    for rfv in request_views_to_update:
        data_sources_set_to_update.add(rfv.request_source)
    for odfv in odfvs_to_update:
        for v in odfv.source_request_sources.values():
            data_sources_set_to_update.add(v)
    data_sources_to_update = list(data_sources_set_to_update)
    entities_to_update.append(DUMMY_ENTITY)
    self._validate_all_feature_views(views_to_update, odfvs_to_update, request_views_to_update, sfvs_to_update)
    self._make_inferences(data_sources_to_update, entities_to_update, views_to_update, odfvs_to_update, sfvs_to_update, services_to_update)
    for ds in data_sources_to_update:
        self._registry.apply_data_source(ds, project=self.project, commit=False)
    for view in itertools.chain(views_to_update, odfvs_to_update, request_views_to_update, sfvs_to_update):
        self._registry.apply_feature_view(view, project=self.project, commit=False)
    for ent in entities_to_update:
        self._registry.apply_entity(ent, project=self.project, commit=False)
    for feature_service in services_to_update:
        self._registry.apply_feature_service(feature_service, project=self.project, commit=False)
    for validation_references in validation_references_to_update:
        self._registry.apply_validation_reference(validation_references, project=self.project, commit=False)
    entities_to_delete = []
    views_to_delete = []
    sfvs_to_delete = []
    if (not partial):
        entities_to_delete = [ob for ob in objects_to_delete if isinstance(ob, Entity)]
        views_to_delete = [ob for ob in objects_to_delete if ((isinstance(ob, FeatureView) or isinstance(ob, BatchFeatureView)) and (not isinstance(ob, StreamFeatureView)))]
        request_views_to_delete = [ob for ob in objects_to_delete if isinstance(ob, RequestFeatureView)]
        odfvs_to_delete = [ob for ob in objects_to_delete if isinstance(ob, OnDemandFeatureView)]
        sfvs_to_delete = [ob for ob in objects_to_delete if isinstance(ob, StreamFeatureView)]
        services_to_delete = [ob for ob in objects_to_delete if isinstance(ob, FeatureService)]
        data_sources_to_delete = [ob for ob in objects_to_delete if isinstance(ob, DataSource)]
        validation_references_to_delete = [ob for ob in objects_to_delete if isinstance(ob, ValidationReference)]
        for data_source in data_sources_to_delete:
            self._registry.delete_data_source(data_source.name, project=self.project, commit=False)
        for entity in entities_to_delete:
            self._registry.delete_entity(entity.name, project=self.project, commit=False)
        for view in views_to_delete:
            self._registry.delete_feature_view(view.name, project=self.project, commit=False)
        for request_view in request_views_to_delete:
            self._registry.delete_feature_view(request_view.name, project=self.project, commit=False)
        for odfv in odfvs_to_delete:
            self._registry.delete_feature_view(odfv.name, project=self.project, commit=False)
        for sfv in sfvs_to_delete:
            self._registry.delete_feature_view(sfv.name, project=self.project, commit=False)
        for service in services_to_delete:
            self._registry.delete_feature_service(service.name, project=self.project, commit=False)
        for validation_references in validation_references_to_delete:
            self._registry.delete_validation_reference(validation_references.name, project=self.project, commit=False)
    tables_to_delete: List[FeatureView] = ((views_to_delete + sfvs_to_delete) if (not partial) else [])
    tables_to_keep: List[FeatureView] = (views_to_update + sfvs_to_update)
    self._get_provider().update_infra(project=self.project, tables_to_delete=tables_to_delete, tables_to_keep=tables_to_keep, entities_to_delete=(entities_to_delete if (not partial) else []), entities_to_keep=entities_to_update, partial=partial)
    self._registry.commit()
    self._teardown_go_server()
