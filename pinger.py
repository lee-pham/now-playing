import json
import time

import requests

cd = .2
headers = {'content-type': 'application/json'}
for i in range(82):
    data = {
        "id": 10,
        "data": [255, 255, 255, 80, 81]
    }
    res = requests.post('http://127.0.0.1:9916/command', headers=headers, data=json.dumps(data))
    print(res.content)
    time.sleep(cd)
