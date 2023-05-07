import netomaton as ntm
import numpy as np

if (__name__ == '__main__'):
    '\n    This demo is inspired by "Collective dynamics of ‘small-world’ networks", by Duncan J. Watts and \n    Steven H. Strogatz (Nature 393, no. 6684 (1998): 440). Towards the end of the paper, they state: \n    "For cellular automata charged with the computational task of density classification, we find that a simple \n    ‘majority-rule’ running on a small-world graph can outperform all known human and genetic algorithm-generated rules \n    running on a ring lattice." The code below attempts to reproduce the experiment they are referring to.\n    '
    network = ntm.topology.watts_strogatz_graph(n=149, k=8, p=0.5)
    initial_conditions = np.random.randint(0, 2, 149)
    print(('density of 1s: %s' % (np.count_nonzero(initial_conditions) / 149)))
    trajectory = ntm.evolve(initial_conditions=initial_conditions, network=network, activity_rule=ntm.rules.majority_rule, timesteps=149)
    ntm.plot_activities(trajectory)
