import base64
import json
import requests
import cv2


def post(to_send, url, own_id, is_image = False):

    if is_image:
        # encode and send data
        retval, to_send = cv2.imencode('.jpg', to_send)

    value = str(base64.b64encode(to_send))[2:-1]
    data = {"data_base64" : value, "berry_id": own_id}
    headers = {'content-type': 'application/json'}
    res = requests.post(url ,data=json.dumps(data), headers=headers)
    