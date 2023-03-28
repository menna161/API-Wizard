from datetime import datetime
import archon.broker as broker
import archon.exchange.exchanges as exc
import archon.model.models as models
import archon.exchange.deribit.Wrapper as deribit
from datetime import datetime, timezone, timedelta


def convert_time(ts):
    return datetime.utcfromtimestamp((int(ts) / 1000)).strftime('%Y-%m-%d %H:%M:%S')
