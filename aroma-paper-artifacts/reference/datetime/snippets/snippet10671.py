import networkx as nx
import logging
import time
import datetime
import adage.dagstate as dagstate


def validate_finished_dag(dag):
    '\n    check for correct temporal execution order\n\n    :param dag: graph object\n    :return: ``True`` if order correct, ``False`` otherwise\n    '
    for node in dag:
        nodeobj = dag.getNode(node)
        if nodeobj.submit_time:
            for x in dag.predecessors(node):
                prednode = dag.getNode(x)
                if (not (nodeobj.submit_time > prednode.ready_by_time)):
                    log.error('??? apparently {} was submitted before predesessor was ready: {}'.format(nodeobj, prednode))
                    log.error('node was submitted at: {} {}'.format(datetime.datetime.fromtimestamp(nodeobj.submit_time), nodeobj))
                    log.error('predecessor finished at: {} {}'.format(datetime.datetime.fromtimestamp(prednode.ready_by_time), prednode))
                    return False
    return True
