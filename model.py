from ultralytics import YOLO
import os
import json
import shutil

DIR_FILE = os.path.dirname(os.path.abspath(__file__))
DIR_MODEL = os.path.join(DIR_FILE, 'models')
os.makedirs(DIR_MODEL, exist_ok=True)

model = YOLO("yolo11n-seg.pt")

if model:
    print("Success load model")

src = model.ckpt_path        # path model di cache ultralytics
dst = os.path.join(DIR_MODEL, "yolo11n-seg.pt")

shutil.copy(src, dst)
