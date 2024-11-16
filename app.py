from flask import Flask, request, jsonify
from io import BytesIO
from PIL import Image
from eh_board.pipeline.prediction_pipeline import get_board_types
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from eh_board.utils import is_allowed
from concurrent.futures import ProcessPoolExecutor

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app)

executor = ProcessPoolExecutor(max_workers=4)


@limiter.limit("60 per minute")
@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        if "image" not in request.files:
            return jsonify({"error": "No file part"}), 400

        image = request.files.get("image")

        if image.filename == "":
            return jsonify({"error": "No selected file"}), 400

        if image and is_allowed(image.filename):
            try:
                img = Image.open(BytesIO(image.read()))

                board_types = executor.submit(get_board_types, img)
                board_types = board_types.result()

                return jsonify({"board_types": list(board_types)}), 200
            except Exception as e:
                return jsonify({"error": str(e)}), 500
        else:
            return jsonify({"error": "Invalid image format"}), 400
    else:
        return jsonify({"error": "Invalid request method"}), 405


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
