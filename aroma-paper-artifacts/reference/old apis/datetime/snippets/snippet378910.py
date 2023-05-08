import sys, os
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from datetime import timedelta
from playfield import Playfield
import rospy
from std_msgs.msg import Int32
from std_msgs.msg import UInt16
from std_msgs.msg import Int32MultiArray
from std_msgs.msg import Bool
from std_msgs.msg import String
from AutoPinball.srv import get_light, get_lightResponse
from AutoPinball.srv import get_switch, get_switchResponse
from AutoPinball.msg import override_light
from AutoPinball.msg import flip_flipper
import time
import signal
import argparse


def calc_date(seconds_in_future, light):
    if (light.blink_start_time == (- 1)):
        return (datetime.now() + timedelta(seconds=seconds_in_future))
    elif light.on:
        return (light.blink_start_time + timedelta(seconds=(seconds_in_future + ((2 * light.curr_number_blink) * seconds_in_future))))
    elif (not light.on):
        return (light.blink_start_time + timedelta(seconds=(seconds_in_future + (((2 * light.curr_number_blink) - 1) * seconds_in_future))))
