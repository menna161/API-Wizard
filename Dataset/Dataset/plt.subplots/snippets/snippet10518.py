import netomaton as ntm
import numpy as np
from matplotlib import pyplot as plt, animation


def plot_boids(positions, velocities, xlim=(0, 500), ylim=(0, 500)):
    (fig, ax) = plt.subplots(figsize=(8, 8))
    ax.set(xlim=xlim, ylim=ylim, xlabel='$x$ coordinate', ylabel='$y$ coordinate')
    velocity_unit_vectors = calculate_unit_vectors(velocities)
    arrows = ax.quiver(positions[(:, 0)], positions[(:, 1)], velocity_unit_vectors[(:, 0)], velocity_unit_vectors[(:, 1)], scale=25, angles='xy', color='burlywood', pivot='tail')
    labels = []
    for (i, position) in enumerate(positions):
        labels.append(ax.text(position[0], position[1], i))
    return (fig, ax, arrows, labels)
