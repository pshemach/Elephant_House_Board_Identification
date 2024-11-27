from ultralytics import YOLO
import shutil
import os
from eh_board.constant import MODEL_PATH, PRED_IMAGE_SAVE_DIR, CONFIDENCE_THRESHOLD


model = None


def load_model():
    global model
    if model is None:
        model = YOLO(MODEL_PATH)


def seg_image(image):
    load_model()
    if os.path.exists(PRED_IMAGE_SAVE_DIR):
        shutil.rmtree(PRED_IMAGE_SAVE_DIR)

    results = model.predict(image, conf=CONFIDENCE_THRESHOLD)

    return results
