import netomaton as ntm
import numpy as np
import csv
import matplotlib.pyplot as plt

if (__name__ == '__main__'):
    n_neurons = 784
    n_timesteps = 4
    initial_conditions = read_image_activities('./mnist-class3.csv')
    initial_weights = read_weights('./mlp_layer1-2_weights.csv')
    timestep_to_weights = {1: read_weights('./mlp_layer2-3_weights.csv'), 2: read_weights('./mlp_layer3-4_weights.csv'), 3: {}}
    timestep_to_activation = {1: relu, 2: relu, 3: identity}
    network = ntm.Network()
    [network.add_edge(i, j) for i in range(n_neurons) for j in range(n_neurons)]
    set_weights(network, initial_weights)

    def activity_rule(ctx):
        V = 0
        for neighbour_label in ctx.neighbour_labels:
            V += (ctx.connection_states[neighbour_label][0]['weight'] * ctx.activities[neighbour_label])
        activity = timestep_to_activation[ctx.timestep](V)
        return activity

    def topology_rule(ctx):
        curr_network = ctx.network
        new_weights = timestep_to_weights[ctx.timestep]
        set_weights(curr_network, new_weights)
        return curr_network
    trajectory = ntm.evolve(network, initial_conditions=initial_conditions, activity_rule=activity_rule, topology_rule=topology_rule, update_order=ntm.UpdateOrder.ACTIVITIES_FIRST, timesteps=n_timesteps)
    vals = [trajectory[(- 1)].activities[i] for i in range(10)]
    plt.title(('predicted class: %s' % np.argmax(np.log(softmax(vals)))))
    plt.imshow(np.array([initial_conditions[i] for i in range(n_neurons)]).reshape((28, 28)), cmap='gray_r')
    plt.show()
