import numpy as np
from PokerRL.cfr._CFRBase import CFRBase as _CFRBase


def _add_strategy_to_average(self, p_id):

    def _fill(_node):
        if (_node.p_id_acting_next == p_id):
            if (self._iter_counter > self.delay):
                current_weight = np.sum(np.arange((self.delay + 1), (self._iter_counter + 1)))
                new_weight = ((self._iter_counter - self.delay) + 1)
                m_old = (current_weight / (current_weight + new_weight))
                m_new = (new_weight / (current_weight + new_weight))
                _node.data['avg_strat'] = ((m_old * _node.data['avg_strat']) + (m_new * _node.strategy))
                assert np.allclose(np.sum(_node.data['avg_strat'], axis=1), 1, atol=0.0001)
            elif (self._iter_counter == self.delay):
                _node.data['avg_strat'] = np.copy(_node.strategy)
                assert np.allclose(np.sum(_node.data['avg_strat'], axis=1), 1, atol=0.0001)
        for c in _node.children:
            _fill(c)
    for t_idx in range(len(self._trees)):
        _fill(self._trees[t_idx].root)
