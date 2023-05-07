import random
import numpy as np


def random_rule_table(k, r, lambda_val=None, quiescent_state=None, strong_quiescence=False, isotropic=False):
    '\n    Constructs and returns a random rule table, as described in [Langton, C. G. (1990). Computation at the edge of\n    chaos: phase transitions and emergent computation. Physica D: Nonlinear Phenomena, 42(1-3), 12-37.], using\n    the "random-table" method.\n    :param k: the number of cell states\n    :param r: the radius of the cellular automaton neighbourhood\n    :param lambda_val: a real number in (0., 1.), representing the value of lambda; if None, a default value of\n                       1.0 - 1/k will be used, where all states will be represented equally in the rule table\n    :param quiescent_state: the state, a number in {0,...,k - 1}, to use as the quiescent state\n    :param strong_quiescence: if True, all neighbourhood states uniform in cell state i will map to cell state i\n    :param isotropic: if True, all planar rotations of a neighbourhood state will map to the same cell state\n    :return: a tuple containing: a table describing a rule, constructed using the "random-table" table method as\n             described by C. G. Langton, the actual lambda value, and the quiescent state used\n    '
    states = []
    n = ((2 * r) + 1)
    for i in range(0, (k ** n)):
        states.append(np.base_repr(i, k).zfill(n))
    table = {}
    if (lambda_val is None):
        lambda_val = (1.0 - (1.0 / k))
    if (quiescent_state is None):
        quiescent_state = np.random.randint(k, dtype=np.int)
    if (not (0 <= quiescent_state <= (k - 1))):
        raise Exception('quiescent state must be a number in {0,...,k - 1}')
    other_states = [x for x in range(0, k) if (x != quiescent_state)]
    quiescent_state_count = 0
    for state in states:
        if (strong_quiescence and (len(set(state)) == 1)):
            cell_state = int(state[0], k)
            if (cell_state == quiescent_state):
                quiescent_state_count += 1
        else:
            state_reversed = state[::(- 1)]
            if (isotropic and (state_reversed in table)):
                cell_state = table[state_reversed]
                if (cell_state == quiescent_state):
                    quiescent_state_count += 1
            elif (random.random() < (1.0 - lambda_val)):
                cell_state = quiescent_state
                quiescent_state_count += 1
            else:
                cell_state = random.choice(other_states)
        table[state] = cell_state
    actual_lambda_val = (((k ** n) - quiescent_state_count) / (k ** n))
    return (table, actual_lambda_val, quiescent_state)
