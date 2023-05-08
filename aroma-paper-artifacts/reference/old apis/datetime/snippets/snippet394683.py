import datetime
import json
import time
from unittest.mock import patch
import pytest
from feast.usage import RatioSampler, log_exceptions, log_exceptions_and_usage, set_usage_attribute, tracing_span


def call_length_ms(call):
    return ((datetime.datetime.fromisoformat(call['end']) - datetime.datetime.fromisoformat(call['start'])).total_seconds() * (10 ** 3))
