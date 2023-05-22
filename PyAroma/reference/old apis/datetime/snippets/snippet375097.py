import subprocess
import os
import time
import core
import config
import rss
from datetime import datetime, timedelta
from core import Recording


def recordAPT(satellite, end_time):
    print((('AOS ' + satellite.name) + '...'))
    date = datetime.utcnow()
    filename = ((((((config.output_dir + '/') + satellite.name) + '/') + satellite.name) + ' at ') + str(datetime.utcnow()))
    print((("Saving as '" + filename) + "'"))
    command = (((('rtl_fm -f ' + str(satellite.frequency)) + "M -M mbfm -s 60000 -r 48000 - | ffmpeg -f s16le -channels 1 -sample_rate 48k -i pipe:0 -f wav '") + filename) + ".wav'")
    subprocess.Popen([command], shell=1)
    while (end_time >= datetime.utcnow()):
        time.sleep(1)
    subprocess.Popen('killall rtl_fm'.split(' '))
    print((('LOS ' + satellite.name) + '...'))
    time.sleep(10)
    return (filename, date)
