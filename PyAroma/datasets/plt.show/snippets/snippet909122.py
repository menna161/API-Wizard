import random
import unittest
from unittest import mock
import numpy as np
from simulator.helper.plot import draw_population_state_daily, draw_specific_population_state_daily, draw_lockdown_state_daily, draw_new_daily_cases, draw_summary, draw_examples, draw_r0_daily_evolution, chose_draw_plot, draw_r0_evolution


@mock.patch('simulator.helper.plot.plt.show')
def test_error_in_stats(self, mock_plt):
    try:
        draw_population_state_daily(self.get_stats(), True)
    except ValueError:
        self.assertTrue(True)
        return
    self.assertTrue(False)
    assert mock_plt.called
