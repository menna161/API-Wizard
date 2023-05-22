from __future__ import print_function
import rospy
from mongodb_store_msgs.msg import StringPairList, StringPair
import mongodb_store_msgs.srv as dc_srv
import mongodb_store.util as dc_util
from mongodb_store.message_store import MessageStoreProxy
from geometry_msgs.msg import Pose, Point, Quaternion
from std_msgs.msg import Bool
from datetime import *
import platform
import io
import StringIO

if (__name__ == '__main__'):
    rospy.init_node('example_multi_event_log')
    try:
        pose = Pose(Point(0, 1, 2), Quaternion(3, 4, 5, 6))
        point = Point(7, 8, 9)
        quaternion = Quaternion(10, 11, 12, 13)
        result = Bool(True)
        msg_store = MessageStoreProxy(collection='pose_results')
        stored = []
        stored.append([pose._type, msg_store.insert(pose)])
        stored.append([point._type, msg_store.insert(point)])
        stored.append([quaternion._type, msg_store.insert(quaternion)])
        stored.append([result._type, msg_store.insert(result)])
        spl = StringPairList()
        for pair in stored:
            spl.pairs.append(StringPair(pair[0], pair[1]))
        meta = {}
        meta['description'] = "this wasn't great"
        meta['result_time'] = datetime.utcfromtimestamp(rospy.get_rostime().to_sec())
        msg_store.insert(spl, meta=meta)
        results = msg_store.query(StringPairList._type)
        for (message, meta) in results:
            if ('description' in meta):
                print(('description: %s' % meta['description']))
            print(('result time (UTC from rostime): %s' % meta['result_time']))
            print(('inserted at (UTC from rostime): %s' % meta['inserted_at']))
            pose = msg_store.query_id(message.pairs[0].second, Pose._type)
            point = msg_store.query_id(message.pairs[1].second, Point._type)
            quaternion = msg_store.query_id(message.pairs[2].second, Quaternion._type)
            result = msg_store.query_id(message.pairs[3].second, Bool._type)
    except rospy.ServiceException as e:
        print(('Service call failed: %s' % e))
