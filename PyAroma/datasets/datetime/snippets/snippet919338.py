from dateutil.parser import parse
from db.Remind import Remind, Base
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Boolean, cast, Date
from sqlalchemy import desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.constants import DATETIME_FORMAT, LAST_REMIND_TIME, LIST_ALL_FLAG, LIST_WEEK_FLAG, START_WEEK_FORMAT, END_WEEK_FORMAT
import datetime
import json
import logging
import os


def check_remind(*time):
    logger.info('Checking reminds...')
    session = Session()
    current_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
    if (not time):
        remind_time = current_time
        remind = session.query(Remind).filter_by(remind_time=remind_time).filter_by(expired=False).filter_by(done=False).all()
    elif (time[0] <= LAST_REMIND_TIME):
        remind_time = (datetime.datetime.strptime(current_time, DATETIME_FORMAT) - datetime.timedelta(minutes=time[0])).strftime(DATETIME_FORMAT)
        remind = session.query(Remind).filter_by(remind_time=remind_time).filter_by(expired=False).filter_by(done=False).all()
        logger.info('Checking NONEXPIRED...')
    else:
        delta = (datetime.datetime.strptime(current_time, DATETIME_FORMAT) - datetime.timedelta(minutes=time[0])).strftime(DATETIME_FORMAT)
        logger.info(('delta time: ' + delta))
        remind = session.query(Remind).filter_by(expired=False).filter_by(done=False).filter((Remind.remind_time <= delta)).all()
        remind_j = json.loads(json.dumps(remind, cls=RemindEncoder, indent=4))
        expire_remind(remind)
        logger.info('expiring remind')
        return ('expired', remind_j)
    remind_j = json.loads(json.dumps(remind, cls=RemindEncoder, indent=4))
    if remind_j:
        return remind_j
    session.close()
