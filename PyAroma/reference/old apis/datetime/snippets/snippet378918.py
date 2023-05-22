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


def local_override_light(override, light):
    if (override == light.override_light):
        pass
    else:
        light.override_light = override
        if (override == 'None'):
            turn_off(light)
            light.curr_number_blink = 0
            light.blink_start_time = (- 1)
            try:
                schedule.remove_job((str(light.pin) + 'ON'))
            except:
                print((('Tried to remove job, but no name - ' + str(light.pin)) + 'NONE'))
        else:
            light.curr_number_blink = 0
            light.blink_start_time = datetime.now()
            try:
                schedule.remove_job((str(light.pin) + 'ON'))
            except:
                print((('Tried to remove job, but no name - ' + str(light.pin)) + 'ON'))
            try:
                schedule.remove_job((str(light.pin) + 'OFF'))
            except:
                print((('Tried to remove job, but no name - ' + str(light.pin)) + 'OFF'))
            turn_on(light)
