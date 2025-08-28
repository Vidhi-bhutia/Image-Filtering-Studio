import os
import uuid
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
from werkzeug.utils import secure_filename
from PIL import Image, ImageFilter, ImageEnhance

# ---- Flask setup ----
application = Flask(__name__)
application.secret_key = os.environ.get("SECRET_KEY", "dev-secret")  # ok for demo

# Elastic Beanstalk allows writing to /tmp safely
BASE_TMP = Path("/tmp")
UPLOAD_DIR = BASE_TMP / "uploads"
PROCESSED_DIR = BASE_TMP / "processed"
for p in (UPLOAD_DIR, PROCESSED_DIR):
    p.mkdir(parents=True, exist_ok=True)

ALLOWED_EXT = {"png", "jpg", "jpeg", "webp"}

def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXT

# ---- Filter logic ----
def apply_filters(img: Image.Image, form: dict) -> Image.Image:
    mode = form.get("filter", "none")
    rotate = int(form.get("rotate", 0) or 0)
    flip_h = form.get("flip_h") == "on"
    flip_v = form.get("flip_v") == "on"
    brightness = float(form.get("brightness", 1.0) or 1.0)
    contrast = float(form.get("contrast", 1.0) or 1.0)

    # Base conversions
    if mode == "grayscale":
        img = img.convert("L").convert("RGB")
    elif mode == "blur":
        strength = int(form.get("blur_strength", 2) or 2)
        img = img.filter(ImageFilter.GaussianBlur(radius=max(0, min(strength, 25))))
    elif mode == "contour":
        img = img.filter(ImageFilter.CONTOUR)
    elif mode == "edge_enhance":
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    # else: "none" does nothing

    # Enhancements
    if brightness != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brightness)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)

    # Flips
    if flip_h:
        img = img.transpose(Image.FLIP_LEFT_RIGHT)
    if flip_v:
        img = img.transpose(Image.FLIP_TOP_BOTTOM)

    # Rotation (normalize)
    if rotate % 360 != 0:
        img = img.rotate(-rotate, expand=True)  # negative for UI feel (clockwise)

    return img

# ---- Routes ----
@application.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@application.route("/process", methods=["POST"])
def process():
    file = request.files.get("image")
    if not file or file.filename == "":
        flash("Please choose an image file.")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Unsupported file type. Use PNG/JPG/JPEG/WEBP.")
        return redirect(url_for("index"))

    safe_name = secure_filename(file.filename)
    ext = safe_name.rsplit(".", 1)[1].lower()
    uid = uuid.uuid4().hex
    in_name = f"{uid}_in.{ext}"
    out_name = f"{uid}_out.jpg"  # serve as JPEG for consistency

    in_path = UPLOAD_DIR / in_name
    out_path = PROCESSED_DIR / out_name

    file.save(in_path)

    with Image.open(in_path) as img:
        img = img.convert("RGB")  # standardize
        result = apply_filters(img, request.form)
        # Quality/optimization for web
        result.save(out_path, "JPEG", quality=90, optimize=True)

    return redirect(url_for("serve_processed", filename=out_name))

@application.route("/processed/<path:filename>")
def serve_processed(filename):
    # Simple page that shows the processed image and a back button
    return render_template(
        "index.html",
        processed_url=url_for("processed_file", filename=filename)
    )

@application.route("/processed-file/<path:filename>")
def processed_file(filename):
    # Direct file endpoint used by <img> src
    return send_from_directory(PROCESSED_DIR, filename, as_attachment=False)

# Healthcheck
@application.route("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    # Local dev
    application.run(host="0.0.0.0", port=5000, debug=True)
