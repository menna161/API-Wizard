import json
from types import FunctionType
from typing import Any, Callable, Dict, List
import dill
import great_expectations as ge
import numpy as np
import pandas as pd
from great_expectations.core import ExpectationSuite
from great_expectations.dataset import PandasDataset
from feast.dqm.profilers.profiler import Profile, Profiler, ValidationError, ValidationReport
from feast.protos.feast.core.ValidationProfile_pb2 import GEValidationProfile as GEValidationProfileProto
from feast.protos.feast.core.ValidationProfile_pb2 import GEValidationProfiler as GEValidationProfilerProto
from feast.protos.feast.serving.ServingService_pb2 import FieldStatus


def _prepare_dataset(dataset: PandasDataset) -> PandasDataset:
    dataset_copy = dataset.copy(deep=True)
    for column in dataset.columns:
        if pd.api.types.is_datetime64_any_dtype(dataset[column]):
            dataset_copy[column] = dataset[column].dt.strftime('%Y-%m-%dT%H:%M:%S')
        if (dataset[column].dtype == np.float32):
            dataset_copy[column] = dataset[column].astype(np.float64)
        status_column = f'{column}__status'
        if (status_column in dataset.columns):
            dataset_copy[column] = dataset_copy[column].mask((dataset[status_column] == FieldStatus.NOT_FOUND), np.nan)
    return dataset_copy
