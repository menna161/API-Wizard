from datetime import date, datetime
from decimal import Decimal
import leather
from leather import utils
from leather.ticks.score_time import ScoreTicker, ScoreTimeTicker


def test_microseconds(self):
    ticker = ScoreTimeTicker(datetime(2011, 3, 5, 2, 15, 15, 1000), datetime(2011, 3, 5, 2, 15, 15, 5000))
    self.assertIsInstance(ticker.ticks[0], datetime)
    self.assertIs(ticker._to_unit, utils.to_microsecond_count)
