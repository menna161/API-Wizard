import copy
import dataclasses
import numpy as np
import pandas as pd
from whynot.framework import GenericExperiment, parameter
from whynot.simulators import civil_violence
from whynot import utils


@parameter(name='citizen_vision', default=5, values=list(range(1, 7)), description='How many other citizens each agent can see.')
@parameter(name='agent_density', default=0.8, values=np.arange(0.05, 0.95, 0.1), description='How densely packed are agents on the grid.')
@parameter(name='cop_fraction', default=0.05, values=[0.1, 0.2, 0.3], description='number of cops = floor(num_samples * cop_fraction)')
@parameter(name='arrest_prob_constant', default=0.9, values=[0.6, 1.2, 2.3, 4.6], description='How strong the interaction between agents is.')
@parameter(name='prison_interaction', default=0.4, values=[0.01, 0.05, 0.1, 0.15, 0.2], description='Degree to which regime legitimacy is drawn toward the min while in prison')
def run_civil_violence(citizen_vision, agent_density, cop_fraction, arrest_prob_constant, prison_interaction, num_samples=100, seed=None, show_progress=False, parallelize=True):
    "Run an RCT experiment on ABM civil violence model.\n\n    Each unit in the experiment is an agent in the model. Treatment corresponds to\n    increasing the 'regime_legitimacy' belief of an agent. Although treatment is\n    assigned randomly to each agent, the units interact, which complicates\n    estimation of treatment effects. The `prison_interaction` term controls the\n    strength of agent interaction.\n\n    Outcomes count the number of days each agent spent in active state.\n\n    Parameters\n    ----------\n        citizen_vision: int\n            How many adjacent cells each agent can see.\n        agent_density: float\n            Density of agents on fixed grid size.\n        cop_fraction: float\n            1 / cop_fraction is number of agents for each cop on the grid.\n        arrest_prob_constant: float\n            How strong the effect of other agents is on perception of arrest probability.\n        prison_interaction: float\n            Degree to which agents share regime legitimacy beliefs in prison.\n        num_samples: int\n            Number of agents to use in the experiments.\n        seed: int\n            (Optional) Seed for all randomness in the experiment.\n        show_progress: bool\n            (Optional) Whether or not to display a progress-bar.\n        parallelize: bool\n            (Optional) Whether or not to execute each simulation in parallel.\n\n    Returns\n    -------\n        covariates: np.ndarray\n            Array of shape [num_agents, num_agent_covariates] of agent covariates\n        treatment: np.ndarray\n            Array of shape [num_agents] showing treatment assignment for each agent.\n        outcome: np.ndarray\n            Array of shape [num_agents] with observed outcome for each agent.\n        true_effect: np.ndarray\n            Array of shape [num_agents] with true (marginal) treatment effects for each agent.\n\n    "
    rng = np.random.RandomState(seed)
    num_cops = int(np.floor((cop_fraction * num_samples)))
    num_cells = ((num_samples + num_cops) / agent_density)
    side_length = int(np.ceil(np.sqrt(num_cells)))
    simulator_config = civil_violence.Config(grid_height=side_length, grid_width=side_length, cop_fraction=cop_fraction, arrest_prob_constant=arrest_prob_constant, prison_interaction=prison_interaction)
    agents = sample_agents(rng, num_samples, citizen_vision)
    rct_assignments = (rng.uniform(size=(num_samples,)) < 0.5)
    (outcomes, true_effects) = run_abm_experiment(agents, rct_assignments, simulator_config, rng, parallelize=parallelize, show_progress=show_progress)
    covariates = pd.DataFrame((dataclasses.asdict(a) for a in agents)).values
    treatment = rct_assignments.astype(np.int64)
    return ((covariates, treatment, outcomes), true_effects)
