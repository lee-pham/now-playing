import pprint
import time
from datetime import datetime
from io import BytesIO
from typing import Tuple

from PIL import Image

img = Image.Image

from secrets import refresh_token, base_64
import requests
import json


class Refresh:
    def __init__(self):
        self.refresh_token = refresh_token
        self.base_64 = base_64

    def refresh(self):
        query = "https://accounts.spotify.com/api/token"
        response = requests.post(query,
                                 data={"grant_type": "refresh_token",
                                       "refresh_token": refresh_token},
                                 headers={"Authorization": "Basic " + base_64})

        response_json = response.json()
        print(f'Requested response on {datetime.now()}:\n{pprint.pformat(response_json)}')
        return response_json["access_token"]


a = Refresh()

print('Hello, world!')
token = a.refresh()


def get_currently_playing() -> Tuple[str, img, str, str]:
    response = requests.get("https://api.spotify.com/v1/me/player/currently-playing?market=US", headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    })
    blank_image_url = "https://via.placeholder.com/8/000000/000000"
    http_status_code = response.status_code
    raw_payload = response.content
    if http_status_code not in {200, 204}:
        print("NON 202/204 RECEIVED:", datetime.now(), response, response.content)
        return blank_image_url, Image.open(
            BytesIO(requests.get(blank_image_url).content)), "No song is currently playing.", ""
    if "expired" in str(response):
        print(datetime.now(), response)
        return blank_image_url, Image.open(BytesIO(requests.get(blank_image_url).content)), "", ""

    if not raw_payload:
        return blank_image_url, Image.open(
            BytesIO(requests.get(blank_image_url).content)), "No song is currently playing.", ""
    payload = json.loads(raw_payload)
    if payload:
        if not payload["item"]:
            return blank_image_url, Image.open(BytesIO(requests.get(blank_image_url).content)), "", ""
        uri = payload["item"].get("uri", "")
        song_name = payload["item"].get("name", "")
        album_name = payload["item"]["album"].get("name")
        artist_name = ", ".join([artist.get("name", "") for artist in payload["item"].get("artists", "")])
        information_string = f"Now playing: {song_name} from {album_name} by {artist_name}"
        image_url = payload["item"]["album"]["images"][2].get("url", "")
        image_response = requests.get(image_url)
        album_art = Image.open(BytesIO(image_response.content))
        return image_url, album_art, information_string, uri
    else:
        return blank_image_url, Image.open(
            BytesIO(requests.get(blank_image_url).content)), "No song is currently playing.", ""


def set_pixels(pixel_list):
    headers = {'content-type': 'application/json'}
    data = {
        "id": 16,
        "data": [item for sublist in pixel_list for item in sublist]
    }
    res = requests.post('http://127.0.0.1:9916/command', headers=headers, data=json.dumps(data))
    print(res.content)


def output_song_information(album_art: img) -> None:
    scaled_album_art = album_art.resize((4, 4)).convert("RGB")
    pixels = list(scaled_album_art.getdata())
    set_pixels(pixels)


currently_playing = [1, 2, 3, 4]
c = 0
while True:
    new_song = get_currently_playing()
    if new_song[3] != currently_playing[3]:
        print(new_song[2])
        output_song_information(new_song[1])
        currently_playing = new_song

    c += 1
    if c > 1800:
        a = Refresh()
        token = a.refresh()
        c = 0

    time.sleep(1)

print("Goodbye, world.")
