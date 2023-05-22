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


def _apply_object(self, table: Table, project: str, id_field_name: str, obj: Any, proto_field_name: str, name: Optional[str]=None):
    self._maybe_init_project_metadata(project)
    name = (name or (obj.name if hasattr(obj, 'name') else None))
    assert name, f'name needs to be provided for {obj}'
    with self.engine.connect() as conn:
        update_datetime = datetime.utcnow()
        update_time = int(update_datetime.timestamp())
        stmt = select(table).where((getattr(table.c, id_field_name) == name), (table.c.project_id == project))
        row = conn.execute(stmt).first()
        if hasattr(obj, 'last_updated_timestamp'):
            obj.last_updated_timestamp = update_datetime
        if row:
            values = {proto_field_name: obj.to_proto().SerializeToString(), 'last_updated_timestamp': update_time}
            update_stmt = update(table).where((getattr(table.c, id_field_name) == name)).values(values)
            conn.execute(update_stmt)
        else:
            obj_proto = obj.to_proto()
            if (hasattr(obj_proto, 'meta') and hasattr(obj_proto.meta, 'created_timestamp')):
                obj_proto.meta.created_timestamp.FromDatetime(update_datetime)
            values = {id_field_name: name, proto_field_name: obj_proto.SerializeToString(), 'last_updated_timestamp': update_time, 'project_id': project}
            insert_stmt = insert(table).values(values)
            conn.execute(insert_stmt)
        self._set_last_updated_metadata(update_datetime, project)
