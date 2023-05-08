from __future__ import absolute_import, unicode_literals
import hashlib
import json
import os
import pickle
from builtins import object
from datetime import datetime
from io import BytesIO
from operator import attrgetter
import boto3
import numpy as np
import pandas as pd
import pymysql
from sklearn.model_selection import train_test_split
from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, MetaData, Numeric, String, Text, and_, create_engine, func, inspect
from sqlalchemy.engine.url import URL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.properties import ColumnProperty
from atm.constants import BUDGET_TYPES, CLASSIFIER_STATUS, DATARUN_STATUS, METRICS, PARTITION_STATUS, SCORE_TARGETS, ClassifierStatus, PartitionStatus, RunStatus
from atm.data import load_data
from atm.utilities import base_64_to_object, object_to_base_64


@try_with_session(commit=True)
def from_csv(self, path):
    '\n        Load a snapshot of the ModelHub database from a set of CSVs in the given\n        directory.\n        '
    for (model, table) in [(self.Dataset, 'dataset'), (self.Datarun, 'datarun'), (self.Hyperpartition, 'hyperpartition'), (self.Classifier, 'classifier')]:
        df = pd.read_csv(os.path.join(path, ('%ss.csv' % table)))
        for c in inspect(model).attrs:
            if (not isinstance(c, ColumnProperty)):
                continue
            col = c.columns[0]
            if isinstance(col.type, DateTime):
                df[c.key] = pd.to_datetime(df[c.key], infer_datetime_format=True)
        for (_, r) in df.iterrows():
            for (k, v) in list(r.iteritems()):
                if pd.isnull(v):
                    r[k] = None
            create_func = getattr(self, ('create_%s' % table))
            create_func(**r)
