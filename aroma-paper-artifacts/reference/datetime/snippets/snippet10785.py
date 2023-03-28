import logging
import time
import os
import shutil
import json
import subprocess
from datetime import datetime
import networkx as nx
import adage.visualize as viz
import adage.serialize as serialize
import adage.dagstate as dagstate
import adage.nodestate as nodestate


def initialize(self, adageobj):
    if (not os.path.exists(os.path.dirname(self.logfilename))):
        os.makedirs(os.path.dirname(self.logfilename))
    with open(self.logfilename, 'w') as logfile:
        timenow = datetime.now().isoformat()
        logfile.write('========== ADAGE LOG BEGIN at {} ==========\n'.format(timenow))
    self.update(adageobj)
