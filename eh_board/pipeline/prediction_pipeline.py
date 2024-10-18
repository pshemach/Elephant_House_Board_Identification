from eh_board.models.segment_yolov8 import seg_image
from eh_board.constant import CONFIDENCE_THRESHOLD


def get_board_types(image_path):
    results = seg_image(image_path=image_path)
    board_types = []

    for result in results:
        if result.boxes is not None:
            for box in result.boxes:
                if box.conf > CONFIDENCE_THRESHOLD:
                    class_idx = int(box.cls)
                    class_name = result.names[class_idx]
                    board_types.append([class_name, box.conf.item()])

    # unique_classes = set(board_types)

    return board_types
