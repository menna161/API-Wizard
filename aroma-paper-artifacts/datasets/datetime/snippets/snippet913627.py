from datetime import datetime
from decimal import Decimal
import tradinhood.endpoints as URL
from tradinhood.errors import *
from tradinhood.util import *


@property
def market_open(self):
    'If the market for this stock is open'
    return self.rbh._get_authed((((self.market_url + 'hours/') + datetime.today().isoformat()[:10]) + '/'))['is_open']
