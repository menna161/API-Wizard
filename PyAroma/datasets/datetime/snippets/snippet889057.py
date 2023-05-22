from datetime import date, datetime
from decimal import Decimal
import leather


def test_project(self):
    scale = leather.Temporal(date(2010, 1, 1), date(2014, 1, 1))
    self.assertAlmostEqual(scale.project(date(2011, 1, 1), 0, 20), 5, 1)
    self.assertAlmostEqual(scale.project(date(2012, 1, 1), 0, 20), 10, 1)
    self.assertAlmostEqual(scale.project(date(2009, 1, 1), 0, 20), (- 5), 1)
    scale = leather.Temporal(datetime(2010, 1, 1), datetime(2014, 1, 1))
    self.assertAlmostEqual(scale.project(datetime(2011, 1, 1), 0, 20), 5, 1)
    self.assertAlmostEqual(scale.project(datetime(2012, 1, 1), 0, 20), 10, 1)
    self.assertAlmostEqual(scale.project(datetime(2009, 1, 1), 0, 20), (- 5), 1)
