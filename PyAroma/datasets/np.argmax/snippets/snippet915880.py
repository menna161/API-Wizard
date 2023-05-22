from robonomics_market.signer import bidhash
from robonomics_market.msg import Bid
from web3 import Web3, HTTPProvider
from std_msgs.msg import String
from std_srvs.srv import Empty, EmptyResponse
import rospy
import json
import numpy as np


def update_current_market(self):
    '\n            Market distribution control rule.\n            Choose market by capital proportional robot distribution,\n            ref http://ensrationis.com/smart-factory-and-capital/\n        '
    rospy.loginfo('Input market list is %s', self.market_list)
    cap = [self.investors.call().supply(m) for m in self.market_list]
    rospy.loginfo('Capitalization vector is %s', cap)
    rob = [len(self.robots[m]) for m in self.market_list]
    rospy.loginfo('Real robot distribution is %s', rob)
    err = distribution_error(np.array(cap), np.array(rob))
    rospy.loginfo('Robot distribution error is %s', err)
    maxi = np.argmax(err)
    rospy.loginfo('Maximal error index is %d', maxi)
    self.market.publish(self.market_list[maxi])
