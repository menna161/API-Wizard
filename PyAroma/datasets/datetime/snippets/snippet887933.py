from datetime import datetime
from app.models.model import User
from app.utils.core import db


def my_job():
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
