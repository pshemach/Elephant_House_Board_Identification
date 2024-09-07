from ultralytics import YOLO
import shutil
import os
from eh_board.constant import MODEL_PATH, IMAGE_SAVE_DIR


model = YOLO(MODEL_PATH)

if os.path.exists(IMAGE_SAVE_DIR):
    shutil.rmtree(IMAGE_SAVE_DIR)
    
def seg_image(image_path, save=True):
        results = model.predict(image_path, save=save)
        return results