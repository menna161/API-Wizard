from angstrom import Trajectory, Molecule
import numpy as np
import os


def test_trajectory_slicing_with_random_integers():
    'Tests Trajectory sllicing.'
    benzene_traj = Trajectory(read=benzene_traj_x)
    n_atoms = len(benzene_traj)
    for i in range(5):
        start = np.random.randint(n_atoms)
        stop = np.random.randint(n_atoms)
        step = np.random.randint(1, n_atoms)
        benzene_slice = benzene_traj[start:stop:step]
        indices = range(start, stop, step)
        assert (len(indices) == len(benzene_slice))
        if (len(indices) == 0):
            assert (type(benzene_slice) == list)
        else:
            assert (type(benzene_slice) == Trajectory)
