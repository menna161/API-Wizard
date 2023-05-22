from netomaton import evolve, WolframPhysicsModel, Network
from .rule_test import *


@staticmethod
def _evolve_wolfram_physics_model(config, rules, timesteps):
    model = WolframPhysicsModel(config, rules)
    trajectory = evolve(network=model.network, topology_rule=model.topology_rule, timesteps=timesteps)
    return model.to_configurations(trajectory)
