import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def animate(self, save=False, interval=50, dpi=80, marker='', repeat=False, fps=50):
    (fig, ax) = plt.subplots()
    ax.set_aspect('equal')
    x_vals = [s[0] for s in self.trajectory]
    max_x = np.max(x_vals)
    min_x = np.min(x_vals)
    max_x += (0.05 * (max_x - min_x))
    min_x -= (0.05 * (max_x - min_x))
    y_vals = [s[1] for s in self.trajectory]
    max_y = np.max(y_vals)
    min_y = np.min(y_vals)
    max_y += (0.05 * (max_y - min_y))
    min_y -= (0.05 * (max_y - min_y))

    def update(t):
        plt.plot(self.trajectory[t][0], self.trajectory[t][1], marker=marker, color='black')
        if ((t == (len(self.trajectory) - 1)) and repeat):
            ax.clear()
            ax.xaxis.set_ticklabels([])
            ax.yaxis.set_ticklabels([])
            ax.set_xticks([])
            ax.set_yticks([])
            plt.xlim(min_x, max_x)
            plt.ylim(min_y, max_y)
    ani = animation.FuncAnimation(fig, update, frames=len(self.trajectory), interval=interval, save_count=len(self.trajectory), repeat=repeat)
    plt.xlim(min_x, max_x)
    plt.ylim(min_y, max_y)
    plt.gca().axes.xaxis.set_ticklabels([])
    plt.gca().axes.yaxis.set_ticklabels([])
    plt.xticks([])
    plt.yticks([])
    if save:
        ani.save('turtle.gif', dpi=dpi, writer='imagemagick', fps=fps)
    plt.show()
