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
def complete_classifier(self, classifier_id, model_location, metrics_location, cv_score, cv_stdev, test_score):
    "\n        Set all the parameters on a classifier that haven't yet been set, and mark\n        it as complete.\n        "
    classifier = self.session.query(self.Classifier).get(classifier_id)
    classifier.model_location = model_location
    classifier.metrics_location = metrics_location
    classifier.cv_judgment_metric = cv_score
    classifier.cv_judgment_metric_stdev = cv_stdev
    classifier.test_judgment_metric = test_score
    classifier.end_time = datetime.now()
    classifier.status = ClassifierStatus.COMPLETE
