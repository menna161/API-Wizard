import copy
import dataclasses
import numpy as np
import pandas as pd
from whynot.framework import GenericExperiment, parameter
from whynot.simulators import civil_violence
from whynot import utils


def run_abm_experiment(agents, treatment_assignments, config, rng, parallelize, show_progress=True):
    'Run an agent-based modeling experiment.\n\n    We run (in parallel) the agent based model for the given treatment assignments to\n    simulate a causal experiment. To obtain ground truth counterfactuals, we run\n    repeatedly run the simulator with the same random seed where (1) no agent i\n    treated [baseline] and (2) where only agent i is treated for i=1, 2, ...\n    Thus, the reported ground truth effects are really the marginal causal\n    effects.\n\n    Parameters\n    ----------\n        agents: list\n            List of whynot.simulators.civil_violence.Agent\n        treatment_assignments: np.ndarray\n            Array of shape [num_agents] indicating whether or not each agent is treated.\n        config: whynot.simulators.civil_violence.Config\n            Simulator parameters to use for each run.\n        rng: np.random.RandomState\n            random number generate to use for all randomness\n        parallelize: bool\n            Whether or not to execute each simulation in parallel.\n        show_progress: bool\n            Whether or not to display a progress-bar\n\n    Returns\n    -------\n        observed_outcomes: np.ndarray\n            Array of shape [num_agents] showing the observed outcome after\n            performing the RCT experiment for all agents simultaneously.\n        true_effects: np.ndarray\n            Array of shape [num_agents] showing the `true` outcome for each\n            agent. Here, true outcome means the outcome obtained by contrasting\n            the experiment where no agent is treated and only agent i is treated.\n\n    '
    baseline_assignments = np.zeros_like(treatment_assignments)
    counterfactual_assignments = []
    for idx in range(len(agents)):
        one_hot = np.zeros_like(treatment_assignments)
        one_hot[idx] = 1.0
        counterfactual_assignments.append(one_hot)
    assignments = ([treatment_assignments, baseline_assignments] + counterfactual_assignments)
    seed = rng.randint(0, 99999)
    parallel_args = [(agents, config, assign, seed) for assign in assignments]
    if parallelize:
        runs = utils.parallelize(run_simulator, parallel_args, show_progress=show_progress)
    else:
        runs = [run_simulator(*args) for args in parallel_args]
    observed_outcomes = runs[0].days_active.values
    baseline = runs[1].days_active.values
    true_effects = []
    for (idx, run) in enumerate(runs[2:]):
        effect = (run.days_active.values - baseline)
        true_effects.append(effect[idx])
    true_effects = np.array(true_effects)
    return (observed_outcomes, true_effects)
