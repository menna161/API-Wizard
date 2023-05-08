import uuid
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from threading import Lock
from typing import Any, Callable, List, Optional, Set, Union
from sqlalchemy import BigInteger, Column, LargeBinary, MetaData, String, Table, create_engine, delete, insert, select, update
from sqlalchemy.engine import Engine
from feast import usage
from feast.base_feature_view import BaseFeatureView
from feast.data_source import DataSource
from feast.entity import Entity
from feast.errors import DataSourceObjectNotFoundException, EntityNotFoundException, FeatureServiceNotFoundException, FeatureViewNotFoundException, SavedDatasetNotFound, ValidationReferenceNotFound
from feast.feature_service import FeatureService
from feast.feature_view import FeatureView
from feast.infra.infra_object import Infra
from feast.infra.registry import proto_registry_utils
from feast.infra.registry.base_registry import BaseRegistry
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.project_metadata import ProjectMetadata
from feast.protos.feast.core.DataSource_pb2 import DataSource as DataSourceProto
from feast.protos.feast.core.Entity_pb2 import Entity as EntityProto
from feast.protos.feast.core.FeatureService_pb2 import FeatureService as FeatureServiceProto
from feast.protos.feast.core.FeatureView_pb2 import FeatureView as FeatureViewProto
from feast.protos.feast.core.InfraObject_pb2 import Infra as InfraProto
from feast.protos.feast.core.OnDemandFeatureView_pb2 import OnDemandFeatureView as OnDemandFeatureViewProto
from feast.protos.feast.core.Registry_pb2 import Registry as RegistryProto
from feast.protos.feast.core.RequestFeatureView_pb2 import RequestFeatureView as RequestFeatureViewProto
from feast.protos.feast.core.SavedDataset_pb2 import SavedDataset as SavedDatasetProto
from feast.protos.feast.core.StreamFeatureView_pb2 import StreamFeatureView as StreamFeatureViewProto
from feast.protos.feast.core.ValidationProfile_pb2 import ValidationReference as ValidationReferenceProto
from feast.repo_config import RegistryConfig
from feast.request_feature_view import RequestFeatureView
from feast.saved_dataset import SavedDataset, ValidationReference
from feast.stream_feature_view import StreamFeatureView


def refresh(self, project: Optional[str]=None):
    if project:
        project_metadata = proto_registry_utils.get_project_metadata(registry_proto=self.cached_registry_proto, project=project)
        if project_metadata:
            usage.set_current_project_uuid(project_metadata.project_uuid)
        else:
            proto_registry_utils.init_project_metadata(self.cached_registry_proto, project)
    self.cached_registry_proto = self.proto()
    self.cached_registry_proto_created = datetime.utcnow()
