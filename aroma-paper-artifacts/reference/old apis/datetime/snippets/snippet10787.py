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


def update(self, adageobj):
    dag = adageobj.dag
    with open(self.logfilename, 'a') as logfile:
        logfile.write('---------- snapshot at {}\n'.format(datetime.now().isoformat()))
        for node in nx.topological_sort(dag):
            nodeobj = dag.getNode(node)
            submitted = (nodeobj.submit_time is not None)
            logfile.write('name: {} obj: {} submitted: {}\n'.format(nodeobj.name, nodeobj, submitted))
