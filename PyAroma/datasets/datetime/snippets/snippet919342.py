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


def _get_last_remind(chat_id, *id):
    session = Session()
    current_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
    if (not id):
        remind = session.query(Remind).filter_by(chat_id=chat_id).filter_by(done=False, expired=False).filter((Remind.remind_time <= current_time)).order_by(desc(Remind.remind_time)).first()
    elif id:
        remind = session.query(Remind).filter_by(chat_id=chat_id).filter_by(id=id)
    if (remind is not None):
        session.close()
        remind_j = json.loads(json.dumps(remind, cls=RemindEncoder))
        if remind_j:
            return remind_j
