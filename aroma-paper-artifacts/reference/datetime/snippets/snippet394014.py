import logging
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from proto import Message
from feast import usage
from feast.base_feature_view import BaseFeatureView
from feast.data_source import DataSource
from feast.entity import Entity
from feast.errors import ConflictingFeatureViewNames, DataSourceNotFoundException, EntityNotFoundException, FeatureServiceNotFoundException, FeatureViewNotFoundException, ValidationReferenceNotFound
from feast.feature_service import FeatureService
from feast.feature_view import FeatureView
from feast.importer import import_class
from feast.infra.infra_object import Infra
from feast.infra.registry import proto_registry_utils
from feast.infra.registry.base_registry import BaseRegistry
from feast.infra.registry.registry_store import NoopRegistryStore
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.project_metadata import ProjectMetadata
from feast.protos.feast.core.Registry_pb2 import Registry as RegistryProto
from feast.repo_config import RegistryConfig
from feast.repo_contents import RepoContents
from feast.request_feature_view import RequestFeatureView
from feast.saved_dataset import SavedDataset, ValidationReference
from feast.stream_feature_view import StreamFeatureView
from feast.infra.registry.sql import SqlRegistry


def apply_feature_view(self, feature_view: BaseFeatureView, project: str, commit: bool=True):
    feature_view.ensure_valid()
    now = datetime.utcnow()
    if (not feature_view.created_timestamp):
        feature_view.created_timestamp = now
    feature_view.last_updated_timestamp = now
    feature_view_proto = feature_view.to_proto()
    feature_view_proto.spec.project = project
    self._prepare_registry_for_changes(project)
    assert self.cached_registry_proto
    self._check_conflicting_feature_view_names(feature_view)
    existing_feature_views_of_same_type: RepeatedCompositeFieldContainer
    if isinstance(feature_view, StreamFeatureView):
        existing_feature_views_of_same_type = self.cached_registry_proto.stream_feature_views
    elif isinstance(feature_view, FeatureView):
        existing_feature_views_of_same_type = self.cached_registry_proto.feature_views
    elif isinstance(feature_view, OnDemandFeatureView):
        existing_feature_views_of_same_type = self.cached_registry_proto.on_demand_feature_views
    elif isinstance(feature_view, RequestFeatureView):
        existing_feature_views_of_same_type = self.cached_registry_proto.request_feature_views
    else:
        raise ValueError(f'Unexpected feature view type: {type(feature_view)}')
    for (idx, existing_feature_view_proto) in enumerate(existing_feature_views_of_same_type):
        if ((existing_feature_view_proto.spec.name == feature_view_proto.spec.name) and (existing_feature_view_proto.spec.project == project)):
            if (feature_view.__class__.from_proto(existing_feature_view_proto) == feature_view):
                return
            else:
                del existing_feature_views_of_same_type[idx]
                break
    existing_feature_views_of_same_type.append(feature_view_proto)
    if commit:
        self.commit()
