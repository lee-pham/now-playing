import json
import time

import requests

cd = .2
headers = {'content-type': 'application/json'}

for i in range(1):
    data = {
        "id": 10,
        "data": [0, 0, 0, 0, 83]
    }
    res = requests.post('http://127.0.0.1:9916/command', headers=headers, data=json.dumps(data))
    print(res.content)
    time.sleep(cd)

led_square = [
    4, 5, 6, 7, 8,
    19, 20, 21, 22, 23,
    34, 35, 36, 37, 38,
    48, 49, 50, 51, 52,
    62, 63, 64, 65, 66
]

for led in led_square:
    data = {
        "id": 10,
        "data": [255, 255, 255, led, led + 1]
    }
    res = requests.post('http://127.0.0.1:9916/command', headers=headers, data=json.dumps(data))
    print(res.content)
    time.sleep(cd)
