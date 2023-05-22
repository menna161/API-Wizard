import random
import unittest
from unittest import mock
import numpy as np
from simulator.helper.plot import draw_population_state_daily, draw_specific_population_state_daily, draw_lockdown_state_daily, draw_new_daily_cases, draw_summary, draw_examples, draw_r0_daily_evolution, chose_draw_plot, draw_r0_evolution


@mock.patch('simulator.helper.plot.plt.show')
def test_chose_draw_plot(self, mock_plt):
    chose_draw_plot(['pop'], self.get_stats(is_empty=False), True)
    assert mock_plt.called
    chose_draw_plot(['R0'], self.get_stats(is_empty=False), True)
    assert mock_plt.called
    chose_draw_plot(['summ'], self.get_stats(is_empty=False), True)
    assert mock_plt.called
    chose_draw_plot(['lock'], self.get_stats(is_empty=False), True)
    assert mock_plt.called
    chose_draw_plot(['new'], self.get_stats(is_empty=False), True)
    assert mock_plt.called
    chose_draw_plot(['hos'], self.get_stats(is_empty=False), True)
    assert mock_plt.called
