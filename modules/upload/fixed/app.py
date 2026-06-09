from pathlib import Path
from uuid import uuid4

from flask import Blueprint, current_app, render_template, request
from werkzeug.utils import secure_filename


bp = Blueprint(
    "upload_fixed",
    __name__,
    url_prefix="/upload/fixed",
    template_folder="templates",
)

ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def private_upload_root():
    root = Path(current_app.instance_path) / "private_uploads"
    root.mkdir(parents=True, exist_ok=True)
    return root


def detected_image_type(data):
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    return None


def validate_upload(uploaded):
    original_name = secure_filename(uploaded.filename or "")
    suffix = Path(original_name).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        return None, "Only .png, .jpg, and .jpeg files are allowed."

    head = uploaded.stream.read(16)
    uploaded.stream.seek(0)
    detected = detected_image_type(head)
    if detected is None:
        return None, "The file content does not look like a PNG or JPEG image."

    if suffix == ".png" and detected != ".png":
        return None, "The file extension does not match the detected image type."
    if suffix in {".jpg", ".jpeg"} and detected != ".jpg":
        return None, "The file extension does not match the detected image type."

    storage_suffix = ".jpg" if suffix == ".jpeg" else suffix
    return f"{uuid4().hex}{storage_suffix}", None


@bp.route("/", methods=["GET", "POST"])
def upload():
    message = None
    saved_name = None

    if request.method == "POST":
        uploaded = request.files.get("file")
        if not uploaded or not uploaded.filename:
            message = "No file selected."
        else:
            saved_name, error = validate_upload(uploaded)
            if error:
                message = error
            else:
                uploaded.save(private_upload_root() / saved_name)
                message = "Upload accepted and stored with a generated name."

    return render_template("upload_fixed.html", message=message, saved_name=saved_name)
