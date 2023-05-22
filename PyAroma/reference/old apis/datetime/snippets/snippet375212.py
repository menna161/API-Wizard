import datetime, hashlib, hmac
import cv2
import requests
import math
import getpass
import boto3
from botocore.exceptions import ClientError
from video_capture import VideoCapture
from detector import Detector
from viewer import Viewer


def run(self):
    username = input('Enter username: ')
    password = getpass.getpass('Enter Password: ')
    try:
        id_token = self._get_id_token_by_cognito(username, password)
    except ClientError as e:
        if (e.response['Error']['Code'] == 'UserNotFoundException'):
            print('User does not exist')
            return
        elif (e.response['Error']['Code'] == 'NotAuthorizedException'):
            print('Invalid password')
            return
        raise
    while True:
        frame = self.video_capture.read()
        if (frame is None):
            raise RuntimeError('A problem occurred with camera. Cannot read a new image.')
        (face_exists, face_image) = self.detector.detect(frame)
        if face_exists:
            self.viewer.show_checking(face_image)
            area = (face_image.shape[0] * face_image.shape[1])
            if (area > (self.FACE_AREA_THRESHOLD * 2)):
                ratio = math.sqrt((area / (self.FACE_AREA_THRESHOLD * 2)))
                face_image = cv2.resize(face_image, (int((face_image.shape[1] / ratio)), int((face_image.shape[0] / ratio))))
            (_, encoded_face_image) = cv2.imencode('.jpg', face_image)
            try:
                endpoint = ('https://' + self.API_ENDPOINT)
                t = datetime.datetime.utcnow()
                amz_date = t.strftime('%Y%m%dT%H%M%SZ')
                headers = {'Content-Type': 'image/jpg', 'X-Amz-Date': amz_date, 'Authorization': id_token}
                request_parameters = encoded_face_image.tostring()
                res = requests.post(endpoint, data=request_parameters, headers=headers).json()
                print(res)
                result = res['result']
            except Exception as e:
                print(e)
            else:
                if (result == 'OK'):
                    name = res['name']
                    similarity = res['similarity']
                    if (similarity > self.FACE_SIMILARITY_THRESHOLD):
                        self._update_name_list()
                        if (name not in [d.get('name') for d in self.recent_name_list]):
                            self.registered_name_set.add(name)
                            self.recent_name_list.append({'name': name, 'timestamp': datetime.datetime.now()})
                            self.viewer.show_welcome(face_image, name)
        else:
            self.viewer.show_next()
        key = cv2.waitKey(1)
        if (key == ord('q')):
            raise RuntimeError("key 'q' is pressed")
