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
def mark_classifier_errored(self, classifier_id, error_message):
    "\n        Mark an existing classifier as having errored and set the error message. If\n        the classifier's hyperpartiton has produced too many erring classifiers, mark it\n        as errored as well.\n        "
    classifier = self.session.query(self.Classifier).get(classifier_id)
    classifier.error_message = error_message
    classifier.status = ClassifierStatus.ERRORED
    classifier.end_time = datetime.now()
    noh_errors = self.get_number_of_hyperpartition_errors(classifier.hyperpartition_id)
    if (noh_errors > MAX_HYPERPARTITION_ERRORS):
        self.mark_hyperpartition_errored(classifier.hyperpartition_id)
