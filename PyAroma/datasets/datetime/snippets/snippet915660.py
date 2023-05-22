import cfnresponse, logging, traceback, boto3, datetime, json
from dateutil.tz import tzlocal


def date_2_string(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
