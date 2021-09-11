import platform
import pprint
import time
from datetime import datetime
from io import BytesIO
from typing import Tuple

from PIL import Image

img = Image.Image

is_rpi = platform.system() == "Linux"
if is_rpi:
    from sense_hat import SenseHat

    sense = SenseHat()

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


def get_currently_playing(token: str) -> Tuple[str, img, str, str]:
    r = requests.get("https://api.spotify.com/v1/me/player/currently-playing?market=US", headers={
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }).content
    blank_image_url = "https://via.placeholder.com/8/000000/000000"
    if r == b"":
        return blank_image_url, Image.open(
            BytesIO(requests.get(blank_image_url).content)), "No song is currently playing.", ""
    response = json.loads(r)
    if "expired" in str(response):
        return blank_image_url, Image.open(BytesIO(requests.get(blank_image_url).content)), "", ""
    if response.get("item", None) is None or response == {}:
        return blank_image_url, Image.open(BytesIO(requests.get(blank_image_url).content)), "", ""
    uri = response["item"].get("uri", "")
    song_name = response["item"].get("name", "")
    album_name = response["item"]["album"].get("name")
    artist_name = ", ".join([artist.get("name", "") for artist in response["item"].get("artists", "")])
    information_string = f"Now playing: {song_name} from {album_name} by {artist_name}"
    image_url = response["item"]["album"]["images"][2].get("url", "")
    image_response = requests.get(image_url)
    album_art = Image.open(BytesIO(image_response.content))

    return image_url, album_art, information_string, uri


def output_song_information(album_art: img, os: bool) -> None:
    scaled_album_art = album_art.resize((8, 8)).convert("RGB")
    pixels = list(scaled_album_art.getdata())
    # print(pixels)
    if os:
        sense.set_pixels(pixels)
    else:
        scaled_album_art.show()


currently_playing = [1, 2, 3, 4]
c = 0
while True:
    new_song = get_currently_playing(token)
    if new_song[3] != currently_playing[3]:
        output_song_information(new_song[1], is_rpi)
        print(new_song[2])
        currently_playing = new_song

    c += 1
    if c > 3500:
        token = a.refresh()
        c = 0

    time.sleep(1)

print("Goodbye, world.")
