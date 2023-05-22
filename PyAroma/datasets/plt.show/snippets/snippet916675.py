
import threading
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
import numpy as np
import time
from pylab import *
import simulator
import Util
from geometry_msgs.msg import Pose, Twist
from simulator_util import DraggablePoint
randimg = np.random.rand(100, 100)
img = plt.imshow(image, extent=[4, 16, 5, 25], zorder=0, interpolation='nearest')
sim = simulator.Simulator()
pose1 = Pose()
pose1.position.x = 5
pose1.position.y = 5
sim.create_robot('0', pose1, [0, 255, 0])
pose2 = Pose()
pose2.position.x = 6
pose2.position.y = 8
sim.create_robot('1', pose2, [255, 0, 0])
ones_matrix = np.zeros((40, 40, 4))
rand_matrix = np.around(np.random.rand(40, 40))
ones_matrix[(:, :, 3)] = rand_matrix
sim.plot_image(ones_matrix, [0, 20, 0, 20])
plt.draw()
plt.show()
