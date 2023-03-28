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


def flipper_on(flipper, time_util_off=(- 1)):
    if flipper.on:
        return
    flipper.on = True
    flipper.last_time_on = rospy.get_rostime().to_sec()
    flipper_pub.publish(flipper.flipper_num)
    if (time_util_off > 0):
        try:
            schedule.add_job(flipper_off, 'date', run_date=(datetime.now() + timedelta(seconds=time_util_off)), args=[flipper], id=(str(flipper.flipper_num) + 'OFF'))
        except:
            print(('Tried to schedule flipper off: ' + str(flipper.flipper_num)))
    elif (time_util_off == 0):
        pass
    else:
        try:
            schedule.add_job(flipper_off, 'date', run_date=(datetime.now() + timedelta(seconds=flipper.general_flipper_on_time)), args=[flipper], id=(str(flipper.flipper_num) + 'OFF'))
        except:
            print(('Tried to schedule flipper off: ' + str(flipper.flipper_num)))
