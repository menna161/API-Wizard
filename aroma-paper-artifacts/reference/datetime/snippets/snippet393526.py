import copy
import warnings
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Type
from google.protobuf.duration_pb2 import Duration
from typeguard import typechecked
from feast import utils
from feast.base_feature_view import BaseFeatureView
from feast.data_source import DataSource, KafkaSource, KinesisSource, PushSource
from feast.entity import Entity
from feast.feature_view_projection import FeatureViewProjection
from feast.field import Field
from feast.protos.feast.core.FeatureView_pb2 import FeatureView as FeatureViewProto
from feast.protos.feast.core.FeatureView_pb2 import FeatureViewMeta as FeatureViewMetaProto
from feast.protos.feast.core.FeatureView_pb2 import FeatureViewSpec as FeatureViewSpecProto
from feast.protos.feast.core.FeatureView_pb2 import MaterializationInterval as MaterializationIntervalProto
from feast.types import from_value_type
from feast.usage import log_exceptions
from feast.value_type import ValueType


@property
def most_recent_end_time(self) -> Optional[datetime]:
    '\n        Retrieves the latest time up to which the feature view has been materialized.\n\n        Returns:\n            The latest time, or None if the feature view has not been materialized.\n        '
    if (len(self.materialization_intervals) == 0):
        return None
    return max([interval[1] for interval in self.materialization_intervals])
