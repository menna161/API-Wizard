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


def finalize(self, adageobj):
    with open(self.logfilename, 'a') as logfile:
        self.update(adageobj)
        timenow = datetime.now().isoformat()
        logfile.write('========== ADAGE LOG END at {} ==========\n'.format(timenow))
