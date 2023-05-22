import sys
import os
from datetime import datetime, timedelta
import Globals
from User import User
from Context import Context
from Enumerations import Button, Mode


def readFrequencyFile(self):
    input_frequencies_file = open(sys.argv[2], 'r')
    lines = input_frequencies_file.readlines()
    count = 0
    for line in lines:
        row = line.split(',')
        timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
        c = Context(timestamp)
        button_freq_list = []
        mode_freq_list = []
        for i in range(1, 9):
            button_freq_list.append(float(row[i]))
        mode_freq_list.append(float(row[9]))
        mode_freq_list.append(float(row[10]))
        c.populateFromFile(button_freq_list, mode_freq_list, int(row[11]), float(row[12]))
        self.context_history.append(c)
        count += 1
        if ((count % 10000) == 0):
            print((('Finished Reading Frequency: ' + str(count)) + ' / 270000'))
