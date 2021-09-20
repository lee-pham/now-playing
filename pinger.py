from split_list_into_list_of_len_n_lists import split_list_into_list_of_len_n_lists
from convert_24_bit_to_8_bit import convert_24_bit_to_8_bit
import json
import requests
import time
from random import randint

cd = .21

pixel_list = []
for i in range(82):
    pixel_list.append([randint(0, 255), randint(0, 255), randint(0, 255)])

compressed_pixel_list = convert_24_bit_to_8_bit(pixel_list)
buffer_length = 24
chunked_payload = split_list_into_list_of_len_n_lists(compressed_pixel_list, buffer_length)
for register, chunk in enumerate(chunked_payload):
    headers = {'content-type': 'application/json'}
    data = {
        "id": 16,
        "data": [register] + chunk
    }
    time.sleep(cd)
    res = requests.post('http://127.0.0.1:9916/command', headers=headers, data=json.dumps(data))
    print(res.content)
