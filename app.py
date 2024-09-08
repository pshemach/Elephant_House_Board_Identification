from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os 

from eh_board.constant import IMAGE_SAVE_DIR
from eh_board.pipeline.prediction_pipeline import get_board_types


app = Flask(__name__)

if not os.path.exists(IMAGE_SAVE_DIR):
    os.makedirs(IMAGE_SAVE_DIR)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    image = request.files['image']

    if image.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if image:
        filename = secure_filename(image.filename)
        image_path = os.path.join(IMAGE_SAVE_DIR, filename)
        image.save(image_path)

        board_types = get_board_types(image_path)

        return jsonify({'board_types': list(board_types)}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)