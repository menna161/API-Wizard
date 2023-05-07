import matplotlib.pyplot as plt
import numpy as np
import torch
from matplotlib.animation import FuncAnimation, writers


def save_traj(images, image_goal, gif_path, task):
    (fig, aa) = plt.subplots(1, 2)
    m1 = aa[0].matshow(images[0], cmap=plt.cm.gray, vmin=0.0, vmax=1.0)
    aa[0].set_title('Time step 0')
    aa[0].set_yticklabels([])
    aa[0].set_xticklabels([])
    m2 = aa[1].matshow(image_goal, cmap=plt.cm.gray, vmin=0.0, vmax=1.0)
    aa[1].set_title('goal')
    aa[1].set_yticklabels([])
    aa[1].set_xticklabels([])
    fig.tight_layout()

    def updatemat2(t):
        m1.set_data(images[t])
        aa[0].set_title(('Time step ' + str(t)))
        m2.set_data(image_goal)
        return (m1, m2)
    frames = len(images)
    if (task in ['plane', 'cartpole']):
        fps = 2
    else:
        fps = 20
    anim = FuncAnimation(fig, updatemat2, frames=frames, interval=200, blit=True, repeat=True)
    Writer = writers['imagemagick']
    writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=1800)
    anim.save(gif_path, writer=writer)
    plt.clf()
    plt.cla()
