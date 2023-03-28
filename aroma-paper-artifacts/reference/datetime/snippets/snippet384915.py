import datetime
import logging
from typing import Optional, Dict, Callable
import boto3
from .metric import Metric


def log(self, name: str, dimensions: Optional[Dict[(str, str)]]=None, value: float=1, **kwargs) -> None:
    'Record metric.\n\n        ``dimensions`` are merged with default_dimensions.\n        Keyword arguments are passed to Metric constructor.\n        '
    complete_dimensions = self.default_dimensions.copy()
    complete_dimensions.update((dimensions or {}))
    self._record_metric(Metric(event_time=datetime.datetime.utcnow(), name=name, value=value, dimensions=complete_dimensions, **kwargs))
