from abc import ABCMeta, abstractmethod
from datetime import datetime


def pick(self, connections):
    'Picks a connection with the earliest backoff time.\n\n           As a result, the first connection is picked\n           for as long as it has no backoff time.\n           Otherwise, the connections are tried in a round robin fashion.\n\n        Args:\n            connections (:obj:list): List of\n                :class:`~bigchaindb_driver.connection.Connection` instances.\n\n        '
    if (len(connections) == 1):
        return connections[0]

    def key(conn):
        return (datetime.min if (conn.backoff_time is None) else conn.backoff_time)
    return min(*connections, key=key)
