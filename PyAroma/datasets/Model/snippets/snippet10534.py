import netomaton as ntm

if (__name__ == '__main__'):
    '\n    In this model, a network of agents are connected to eachother in a Euclidean lattice. Each agent \n    possesses a certain amount of "resource". An agent\'s resource can change by picking up resource from \n    a resource layer, and through the receipt of resource from its neighbours. \n\n    An agent represents a cell, and the links between agents represent the flow of resources between cells. (The \n    flow of resources is unidirectional only.)\n\n    This implementation represents process "1", model "a", from the paper:\n    Smith, David MD, et al. "Network automata: Coupling structure and function in dynamic networks."\n    Advances in Complex Systems 14.03 (2011): 317-339.\n    '
    R_E = 80000.0
    timesteps = 100
    width = 200
    height = 200
    compression = False
    persist_network = False
    initial_conditions = ntm.init_simple2d(width, height, val=R_E, dtype=float)
    model = ntm.FungalGrowthModel(R_E, width, height, initial_conditions, seed=20210408)
    trajectory = ntm.evolve(network=model.network, initial_conditions=initial_conditions, timesteps=timesteps, activity_rule=model.activity_rule, topology_rule=model.topology_rule, update_order=model.update_order, copy_network=model.copy_network, compression=compression, persist_network=persist_network)
    ntm.animate_activities(trajectory, shape=(width, height), interval=200, colormap='jet')
