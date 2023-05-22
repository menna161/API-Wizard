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


def create(chat_id, time, text, expired=False, done=False):
    logger.info('Creating remind...')
    session = Session()
    parsed_time = parse(time, dayfirst=True)
    today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:00')
    if (parsed_time > parse(today)):
        remind = Remind(chat_id, parsed_time, text, expired, done)
        session.add(remind)
    else:
        raise Exception
    session.commit()
    session.close()
