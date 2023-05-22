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


def apply_materialization(self, feature_view: FeatureView, project: str, start_date: datetime, end_date: datetime, commit: bool=True):
    self._prepare_registry_for_changes(project)
    assert self.cached_registry_proto
    for (idx, existing_feature_view_proto) in enumerate(self.cached_registry_proto.feature_views):
        if ((existing_feature_view_proto.spec.name == feature_view.name) and (existing_feature_view_proto.spec.project == project)):
            existing_feature_view = FeatureView.from_proto(existing_feature_view_proto)
            existing_feature_view.materialization_intervals.append((start_date, end_date))
            existing_feature_view.last_updated_timestamp = datetime.utcnow()
            feature_view_proto = existing_feature_view.to_proto()
            feature_view_proto.spec.project = project
            del self.cached_registry_proto.feature_views[idx]
            self.cached_registry_proto.feature_views.append(feature_view_proto)
            if commit:
                self.commit()
            return
    for (idx, existing_stream_feature_view_proto) in enumerate(self.cached_registry_proto.stream_feature_views):
        if ((existing_stream_feature_view_proto.spec.name == feature_view.name) and (existing_stream_feature_view_proto.spec.project == project)):
            existing_stream_feature_view = StreamFeatureView.from_proto(existing_stream_feature_view_proto)
            existing_stream_feature_view.materialization_intervals.append((start_date, end_date))
            existing_stream_feature_view.last_updated_timestamp = datetime.utcnow()
            stream_feature_view_proto = existing_stream_feature_view.to_proto()
            stream_feature_view_proto.spec.project = project
            del self.cached_registry_proto.stream_feature_views[idx]
            self.cached_registry_proto.stream_feature_views.append(stream_feature_view_proto)
            if commit:
                self.commit()
            return
    raise FeatureViewNotFoundException(feature_view.name, project)
