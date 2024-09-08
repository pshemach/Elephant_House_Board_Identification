from ultralytics import YOLO
import shutil
import os
from eh_board.constant import MODEL_PATH, PRED_IMAGE_SAVE_DIR


model = YOLO(MODEL_PATH)

def seg_image(image_path, save=True):
        if os.path.exists(PRED_IMAGE_SAVE_DIR):
            shutil.rmtree(PRED_IMAGE_SAVE_DIR)

        results = model.predict(image_path, save=save)

        return results