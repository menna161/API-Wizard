import copy
import functools
import warnings
from datetime import datetime
from types import FunctionType
from typing import Any, Dict, List, Optional, Type, Union
import dill
import pandas as pd
from typeguard import typechecked
from feast.base_feature_view import BaseFeatureView
from feast.batch_feature_view import BatchFeatureView
from feast.data_source import RequestSource
from feast.errors import RegistryInferenceFailure, SpecifiedFeaturesNotPresentError
from feast.feature_view import FeatureView
from feast.feature_view_projection import FeatureViewProjection
from feast.field import Field, from_value_type
from feast.protos.feast.core.OnDemandFeatureView_pb2 import OnDemandFeatureView as OnDemandFeatureViewProto
from feast.protos.feast.core.OnDemandFeatureView_pb2 import OnDemandFeatureViewMeta, OnDemandFeatureViewSpec, OnDemandSource
from feast.protos.feast.core.OnDemandFeatureView_pb2 import UserDefinedFunction as UserDefinedFunctionProto
from feast.type_map import feast_value_type_to_pandas_type, python_type_to_feast_value_type
from feast.usage import log_exceptions
from feast.value_type import ValueType


def infer_features(self):
    '\n        Infers the set of features associated to this feature view from the input source.\n\n        Raises:\n            RegistryInferenceFailure: The set of features could not be inferred.\n        '
    rand_df_value: Dict[(str, Any)] = {'float': 1.0, 'int': 1, 'str': 'hello world', 'bytes': str.encode('hello world'), 'bool': True, 'datetime64[ns]': datetime.utcnow()}
    df = pd.DataFrame()
    for feature_view_projection in self.source_feature_view_projections.values():
        for feature in feature_view_projection.features:
            dtype = feast_value_type_to_pandas_type(feature.dtype.to_value_type())
            df[f'{feature_view_projection.name}__{feature.name}'] = pd.Series(dtype=dtype)
            sample_val = (rand_df_value[dtype] if (dtype in rand_df_value) else None)
            df[f'{feature.name}'] = pd.Series(data=sample_val, dtype=dtype)
    for request_data in self.source_request_sources.values():
        for field in request_data.schema:
            dtype = feast_value_type_to_pandas_type(field.dtype.to_value_type())
            sample_val = (rand_df_value[dtype] if (dtype in rand_df_value) else None)
            df[f'{field.name}'] = pd.Series(sample_val, dtype=dtype)
    output_df: pd.DataFrame = self.udf.__call__(df)
    inferred_features = []
    for (f, dt) in zip(output_df.columns, output_df.dtypes):
        inferred_features.append(Field(name=f, dtype=from_value_type(python_type_to_feast_value_type(f, type_name=str(dt)))))
    if self.features:
        missing_features = []
        for specified_features in self.features:
            if (specified_features not in inferred_features):
                missing_features.append(specified_features)
        if missing_features:
            raise SpecifiedFeaturesNotPresentError(missing_features, inferred_features, self.name)
    else:
        self.features = inferred_features
    if (not self.features):
        raise RegistryInferenceFailure('OnDemandFeatureView', f"Could not infer Features for the feature view '{self.name}'.")
