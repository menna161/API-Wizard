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


def close(user_chat_id, id):
    logger.info('Closing reminds...')
    session = Session()
    current_time = datetime.datetime.now().strftime(DATETIME_FORMAT)
    if (not id):
        remind = session.query(Remind).filter_by(chat_id=user_chat_id).filter_by(done=False).filter((Remind.remind_time <= current_time)).order_by(desc(Remind.remind_time)).first()
        if (remind is not None):
            session.query(Remind).filter_by(chat_id=user_chat_id).filter_by(id=remind.id).update({'done': True}, synchronize_session=False)
            remind_id = remind.id
    else:
        for i in id:
            session.query(Remind).filter_by(chat_id=user_chat_id).filter_by(id=i).update({'done': True}, synchronize_session=False)
        remind_id = id
    session.commit()
    session.close()
    return remind_id
