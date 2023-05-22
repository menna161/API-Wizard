import argparse
import os
import time
import cv2
import numpy as np
import dlib
from utils import CentroidTracker, TrackableObject, Conf
from bounding_box import bounding_box as bb


def main():
    counted_objectID = []
    (H, W) = (None, None)
    '\n     initialize our centroid tracker, then initialize a lost to store\n     each of our dlib correlation trackers, followed by a dictionary to \n     map each unique object ID to a TrackableOject \n    '
    ct = CentroidTracker(maxDisappeared=conf['max_disappear'], maxDistance=conf['max_distance'])
    trackers = []
    trackableObjects = {}
    totalFrame = 0
    net = load_model()
    cap = cv2.VideoCapture(args['video'])
    time.sleep(1)
    (_, frame) = cap.read()
    count_line = [(0, (frame.shape[0] - conf['line_coordinate'])), (frame.shape[1], (frame.shape[0] - conf['line_coordinate']))]
    car_count = 0
    if args['save']:
        video_size = ((frame.shape[1] + 250), frame.shape[0])
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        writer = cv2.VideoWriter('processed_video.avi', fourcc, 24, video_size)
    while True:
        (ret, frame) = cap.read()
        if (frame is None):
            break
        origin_frame = frame.copy()
        frame = frame[(:((frame.shape[0] - conf['line_coordinate']) - 25), :, :)]
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        if ((W is None) or (H is None)):
            (H, W) = frame.shape[:2]
        '\n        initialize our list of bounding box rectangles returned by \n        either (1) our object detector or (2) the correlation trackers\n        '
        rects = []
        '\n        check to see if we should run a more computationally expensive\n        object detection method to add our tracker\n        '
        if ((totalFrame % conf['track_object']) == 0):
            trackers = []
            '\n            convert the frame to a blob and pass the blob \n            through the netwrok and obtain the detections\n            '
            blob = cv2.dnn.blobFromImage(frame, ddepth=cv2.CV_8U)
            net.setInput(blob, scalefactor=(1.0 / 255), mean=[255, 255, 255])
            detections = net.forward()
            for i in np.arange(0, detections.shape[2]):
                '\n                extract the confidence (i.e., probability)\n                associate with the predicton\n                '
                confidence = detections[(0, 0, i, 2)]
                '\n                filter out weak detections by \n                setting a threshold confidence\n                '
                if (confidence > conf['confidence']):
                    '\n                    extract the index of the class label\n                    from detection list\n                    '
                    idx = int(detections[(0, 0, i, 1)])
                    if (CLASSES[idx] != 'car'):
                        continue
                    '\n                    compute the (x,y)-coordinates of the \n                    bounding box for the object\n                    '
                    box = (detections[(0, 0, i, 3:7)] * np.array([W, H, W, H]))
                    (startX, startY, endX, endY) = box.astype('int')
                    '\n                    construct a dlib rectangle object from the bounding\n                    box coordinates and then start the dlib correlation tracker\n                    '
                    tracker = dlib.correlation_tracker()
                    rect = dlib.rectangle(startX, startY, endX, endY)
                    tracker.start_track(rgb, rect)
                    '\n                    add the tracker to our list of trackers\n                    so we can utilize it during skip frames\n                    '
                    trackers.append(tracker)
            '\n        otherwise, we should utilize our object "trackes" rather than \n        object "detectors" to obtain a higher frame preprocessing\n            '
        else:
            for tracker in trackers:
                tracker.update(rgb)
                pos = tracker.get_position()
                post_list = [pos.left(), pos.top(), pos.right(), pos.bottom()]
                [startX, startY, endX, endY] = list(map(int, post_list))
                rects.append((startX, startY, endX, endY))
        '\n        use the centroid tracker to associate the (1) old object\n        centroids with (2) the newly computed object centroids\n        '
        objects = ct.update(rects)
        for ((objectID, centroid), rect) in zip(objects.copy().items(), rects):
            if (objectID in counted_objectID):
                ct.deregister(objectID)
                rects.remove(rect)
                trackers.remove(tracker)
                objects = ct.update(rects)
                break
            else:
                '\n                if centroid of the car cross count line \n                then increment car_count\n                '
                if ((centroid[1] + 60) > count_line[0][1]):
                    rects.remove(rect)
                    trackers.remove(tracker)
                    counted_objectID.append(objectID)
                    ct.deregister(objectID)
                    objects = ct.update(rects)
                    car_count += 1
                    break
            '\n            check to see if a trackable object exists\n            for the current object ID\n            '
            to = trackableObjects.get(objectID, None)
            if (to is None):
                to = TrackableObject(objectID, centroid)
            trackableObjects[objectID] = to
            '\n            draw both the ID of the object and the centroid \n            of the object on the output frame\n            '
            text = 'ID {}'.format(objectID)
            bb.add(origin_frame, rect[0], rect[1], rect[2], rect[3], 'car', 'green')
            cv2.putText(origin_frame, text, ((centroid[0] - 10), (centroid[1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            cv2.circle(origin_frame, (centroid[0], centroid[1]), 4, (0, 255, 0), (- 1))
        blank_region = (np.ones((origin_frame.shape[0], 250, 3), np.uint8) * 255)
        cv2.putText(blank_region, 'No. car(s):', (40, ((origin_frame.shape[0] // 2) - 120)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 3)
        cv2.line(origin_frame, count_line[0], count_line[1], (0, 255, 0), 3)
        cv2.putText(blank_region, str(car_count), (40, (origin_frame.shape[0] // 2)), cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 0, 0), 3)
        stack_image = np.concatenate((origin_frame, blank_region), axis=1)
        cv2.imshow('Final result', stack_image)
        if args['save']:
            writer.write(stack_image)
        key = (cv2.waitKey(1) & 255)
        if (key == 27):
            break
        totalFrame += 1
    cap.release()
    cv2.destroyAllWindows()
    if args['save']:
        writer.release()
