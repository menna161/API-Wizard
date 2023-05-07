from datetime import date, datetime
from decimal import Decimal
import leather
from leather import utils
from leather.ticks.score_time import ScoreTicker, ScoreTimeTicker


def test_months_datetime(self):
    ticker = ScoreTimeTicker(datetime(2011, 3, 1), datetime(2011, 7, 1))
    self.assertIsInstance(ticker.ticks[0], datetime)
    self.assertIs(ticker._to_unit, utils.to_month_count)
