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


def get_reminds(user_chat_id, interval):
    logger.info('Getting reminds...')
    session = Session()
    if (interval == ''):
        reminds_list = session.query(Remind).filter_by(chat_id=user_chat_id).filter((cast(Remind.remind_time, Date) == datetime.datetime.today().date())).order_by(Remind.remind_time).all()
        json_data = json.loads(json.dumps(reminds_list, cls=RemindEncoder, indent=4))
    elif (interval == LIST_ALL_FLAG):
        reminds_list = session.query(Remind).filter_by(chat_id=user_chat_id).order_by(Remind.remind_time).all()
    elif (interval == LIST_WEEK_FLAG):
        today = datetime.datetime.today()
        weekday = today.weekday()
        mon = (today - datetime.timedelta(days=weekday)).strftime(START_WEEK_FORMAT)
        sun = (today + datetime.timedelta(days=(6 - weekday))).strftime(END_WEEK_FORMAT)
        reminds_list = session.query(Remind).filter_by(chat_id=user_chat_id).filter((cast(Remind.remind_time, Date) >= mon), (cast(Remind.remind_time, Date) <= sun)).order_by(Remind.remind_time).all()
    elif interval.isdigit():
        reminds_list = session.query(Remind).filter_by(chat_id=user_chat_id).order_by(desc(Remind.remind_time)).limit(interval).all()
    json_data = json.loads(json.dumps(reminds_list, cls=RemindEncoder, indent=4))
    session.close()
    if json_data:
        return json_data
