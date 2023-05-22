import math
import threading
import matplotlib.pyplot as plt
import numpy as np
import rospy
import time
from geometry_msgs.msg import Pose, Twist
from matplotlib import patches
from matplotlib.collections import PatchCollection
from nav_msgs.msg import Odometry, OccupancyGrid
from nav_msgs.srv import GetMap
from voronoi_hsi.msg import VoronoiTesselation
from voronoi_hsi.srv import *
import Util
import simulator_util


def start(self):
    self.physics_t.start()
    self.visual_t.start()
    plt.show()
