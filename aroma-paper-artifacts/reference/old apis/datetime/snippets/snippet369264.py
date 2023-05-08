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
def mark_datarun_complete(self, datarun_id):
    "\n        Set the status of the Datarun to COMPLETE and set the 'end_time' field\n        to the current datetime.\n        "
    datarun = self.get_datarun(datarun_id)
    datarun.status = RunStatus.COMPLETE
    datarun.end_time = datetime.now()
