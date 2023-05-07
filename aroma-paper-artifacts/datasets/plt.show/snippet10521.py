import netomaton as ntm
import numpy as np
from matplotlib import pyplot as plt, animation

if (__name__ == '__main__'):
    num_boids = 10
    timesteps = 500
    visual_range = 70
    protected_range = 12
    turn_factor = 2
    centering_factor = 0.0005
    avoid_factor = 0.05
    matching_factor = 0.05
    max_speed = 4
    min_speed = 3
    min_position = (10, 100)
    max_position = (100, 200)
    min_velocity = (0, (- 2))
    max_velocity = (1, 2)
    network = ntm.Network(n=num_boids)
    np.random.seed(43)
    pos = np.random.uniform(min_position, max_position, size=(num_boids, 2))
    vel = np.random.uniform(min_velocity, max_velocity, size=(num_boids, 2))
    initial_conditions = {n: (pos[n][0], pos[n][1], vel[n][0], vel[n][1]) for n in network.nodes}

    def activity_rule(ctx):
        (x, y, vx, vy) = ctx.current_activity
        (x_avg, y_avg, vx_avg, vy_avg, close_dx, close_dy, visual_boids) = (0, 0, 0, 0, 0, 0, 0)
        for (x_j, y_j, vx_j, vy_j) in ctx.neighbourhood_activities:
            dist = np.linalg.norm((np.array([x, y]) - np.array([x_j, y_j])))
            if (dist < protected_range):
                close_dx += (x - x_j)
                close_dy += (y - y_j)
            else:
                x_avg += x_j
                y_avg += y_j
                vx_avg += vx_j
                vy_avg += vy_j
                visual_boids += 1
        if (visual_boids > 0):
            x_avg = (x_avg / visual_boids)
            y_avg = (y_avg / visual_boids)
            vx_avg = (vx_avg / visual_boids)
            vy_avg = (vy_avg / visual_boids)
            vx = ((vx + ((x_avg - x) * centering_factor)) + ((vx_avg - vx) * matching_factor))
            vy = ((vy + ((y_avg - y) * centering_factor)) + ((vy_avg - vy) * matching_factor))
        vx = (vx + (close_dx * avoid_factor))
        vy = (vy + (close_dy * avoid_factor))
        if (y > 450):
            vy = (vy - turn_factor)
        if (x > 450):
            vx = (vx - turn_factor)
        if (x < 50):
            vx = (vx + turn_factor)
        if (y < 50):
            vy = (vy + turn_factor)
        speed = np.sqrt(((vx * vx) + (vy * vy)))
        if (speed < min_speed):
            vx = ((vx / speed) * min_speed)
            vy = ((vy / speed) * min_speed)
        if (speed > max_speed):
            vx = ((vx / speed) * max_speed)
            vy = ((vy / speed) * max_speed)
        return ((x + vx), (y + vy), vx, vy)

    def topology_rule(ctx):
        new_network = ctx.network.copy()
        n_nodes = len(ctx.network.nodes)
        for i in range(n_nodes):
            for j in range((i + 1), n_nodes):
                (x_i, y_i, _, _) = ctx.activities[i]
                (x_j, y_j, _, _) = ctx.activities[j]
                dist = np.linalg.norm((np.array([x_i, y_i]) - np.array([x_j, y_j])))
                if (dist < visual_range):
                    new_network.add_edge(i, j)
                elif new_network.has_edge(i, j):
                    new_network.remove_edge(i, j)
        return new_network
    trajectory = ntm.evolve(network=network, initial_conditions=initial_conditions, topology_rule=topology_rule, activity_rule=activity_rule, timesteps=timesteps, update_order=ntm.UpdateOrder.TOPOLOGY_FIRST)
    anim1 = animate_flock(trajectory, num_step=timesteps)
    anim2 = ntm.animate_network(trajectory, with_arrows=False, node_color='burlywood', node_size=150, with_timestep=True, interval=1, show=False)
    plt.show()
