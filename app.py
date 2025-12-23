from flask import Flask, render_template, request, jsonify
import os
import torch
import pickle
from PIL import Image
import base64

# =========================
# Flask configuration
# =========================
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# =========================
# Load BLIP model from .pkl
# =========================
print("=" * 60)
print("LOADING BLIP MODEL (PKL)...")
print("=" * 60)

try:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Load model
    with open("model/blip_model.pkl", "rb") as f:
        model = pickle.load(f)

    # Load processor
    with open("model/blip_processor.pkl", "rb") as f:
        processor = pickle.load(f)

    model.to(device)
    model.eval()

    print("✓ BLIP model loaded successfully")
    print(f"✓ Running on device: {device}")

except Exception as e:
    print(f"✗ ERROR loading BLIP model: {e}")
    raise SystemExit(1)

# =========================
# Utility functions
# =========================
def image_to_base64(image_path):
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def generate_caption(image_path, max_length=30):
    image = Image.open(image_path).convert("RGB")

    # Processor → tensor
    inputs = processor(images=image, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_length=max_length,
            num_beams=4,
            early_stopping=True
        )

    caption = processor.decode(
        output_ids[0],
        skip_special_tokens=True
    )

    return caption

# =========================
# Routes
# =========================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        allowed_ext = {"jpg", "jpeg", "png", "bmp"}
        ext = file.filename.rsplit(".", 1)[-1].lower()

        if ext not in allowed_ext:
            return jsonify({"error": "Invalid file type"}), 400

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        print(f"[INFO] Processing image: {file.filename}")

        caption = generate_caption(filepath)

        img_base64 = image_to_base64(filepath)

        os.remove(filepath)

        return jsonify({
            "success": True,
            "caption": caption,
            "image": f"data:image/jpeg;base64,{img_base64}"
        })

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"error": str(e)}), 500

# =========================
# Run Flask app
# =========================
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
