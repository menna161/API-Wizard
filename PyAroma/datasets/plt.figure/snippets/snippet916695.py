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


def __init__(self):
    self.printing_voronoi = False
    self.robots = {}
    self.physics_time = 0.05
    rospy.init_node('simulator')
    self.vis_time = 0.05
    self.robot_pose_service = rospy.Service('set_robot_pose', SetRobotPose, self.robot_service)
    self.occ_grid_topic = ''
    self.tesselation_topic = ''
    self.robot_param = ''
    self.occ_grid_subscriber = None
    self.tesselation_subscriber = None
    self.voronoi_collection = None
    self.voronoi_axes = None
    self.voronoi_should_draw = False
    self.plot_handle = None
    self.obstacle_collection = None
    self.obstacle_axes = None
    self.fig = plt.figure(1)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis([0, 20, 0, 20])
    self.occ_grid = OccGrid('static_map', self.fig)
    self.occ_grid.get_occ_grid()
    self.fig.canvas.draw()
    self.read_simulator_params()
    self.read_robot_parameters()
    self.physics_t = threading.Thread(target=self.physics_thread)
    self.physics_t.daemon = True
    self.visual_t = threading.Thread(target=self.visual_thread)
    self.visual_t.daemon = True
    self.loop_time = 0
