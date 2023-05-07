from datetime import date, datetime
from decimal import Decimal
import leather
from leather import utils
from leather.ticks.score_time import ScoreTicker, ScoreTimeTicker


def test_hours_for_days(self):
    ticker = ScoreTimeTicker(datetime(2011, 3, 5), datetime(2011, 3, 6))
    self.assertIsInstance(ticker.ticks[0], datetime)
    self.assertIs(ticker._to_unit, utils.to_hour_count)
