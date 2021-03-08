import os, requests
import geocoder # ! pip install geocoder
import math
from skimage import io
from io import BytesIO
import numpy as np
import cv2

# Fields
BASE_API_URL = "https://gisapi.tellusxdp.com"
ASNARO1_SCENE = "/api/v1/asnaro1/scene"
ACCESS_TOKEN = "ご自身のトークンを貼り付けてください"
HEADERS = {"Authorization": "Bearer " + ACCESS_TOKEN}
TARGET_PLACE = "skytree, Tokyo"
SAVE_DIRECTORY="./data/asnaro/"
ZOOM_LEVEL=18
IMG_SYNTH_NUM=6
IMG_BASE_SIZE=256

# Functions
def get_tile_num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def get_scene_list(_get_params={}):
    query = BASE_API_URL + ASNARO1_SCENE
    r = requests.get(query, _get_params, headers=HEADERS)
    if not r.status_code == requests.codes.ok:
        r.raise_for_status()
    return r.json()

def get_scene(_id, _xc, _yc):
    # mkdir
    save_file_name = SAVE_DIRECTORY + _id + ".png"
    if os.path.exists(SAVE_DIRECTORY) == False:
        os.makedirs(SAVE_DIRECTORY)
        
    # download
    save_image = np.zeros((IMG_SYNTH_NUM * IMG_BASE_SIZE, IMG_SYNTH_NUM * IMG_BASE_SIZE, 3))
    for i in range(IMG_SYNTH_NUM):
        for j in range(IMG_SYNTH_NUM):
            query = "/ASNARO-1/" + _id + "/" + str(ZOOM_LEVEL) + "/" + str(_xc-int(IMG_SYNTH_NUM*0.5)+i) + "/" + str(_yc-int(IMG_SYNTH_NUM*0.5)+j) + ".png"        
            r = requests.get(BASE_API_URL + query, headers=HEADERS)
            if not r.status_code == requests.codes.ok:
                r.raise_for_status()
            img = io.imread(BytesIO(r.content))
            save_image[i*IMG_BASE_SIZE:(i+1)*IMG_BASE_SIZE, j*IMG_BASE_SIZE:(j+1)*IMG_BASE_SIZE, :] = img[:, :, 0:3].transpose(1, 0, 2) # [x, y, c] -> [y, x, c]
    save_image = cv2.flip(save_image, 1)
    save_image = cv2.rotate(save_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    cv2.imwrite(save_file_name, save_image)
    print("[DONE]" + save_file_name)
    return


# Entry point
def main():
    # extract slc list around the address
    gc = geocoder.osm(TARGET_PLACE, timeout=5.0) # get latlon
    scene_list = get_scene_list({"min_lat":  gc.latlng[0], "min_lon":  gc.latlng[1], "max_lat":  gc.latlng[0], "max_lon":  gc.latlng[1]})
    for _scene in scene_list:
        #_xc, _yc = get_tile_num(_scene['clat'], _scene['clon'], ZOOM_LEVEL) # center
        _xc, _yc = get_tile_num(gc.latlng[0], gc.latlng[1], ZOOM_LEVEL)
        get_scene(_scene['entityId'], _xc, _yc)

if __name__=="__main__":
       main()
