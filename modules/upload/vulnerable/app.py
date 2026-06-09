from pathlib import Path

from flask import Blueprint, current_app, render_template, request, send_from_directory


bp = Blueprint(
    "upload_vulnerable",
    __name__,
    url_prefix="/upload/vulnerable",
    template_folder="templates",
)


def upload_root():
    root = Path(current_app.instance_path) / "public_uploads"
    root.mkdir(parents=True, exist_ok=True)
    return root


@bp.route("/", methods=["GET", "POST"])
def upload():
    message = None
    file_url = None

    if request.method == "POST":
        uploaded = request.files.get("file")
        if uploaded and uploaded.filename:
            destination = upload_root() / uploaded.filename
            uploaded.save(destination)
            message = f"Saved {uploaded.filename}"
            file_url = f"/upload/vulnerable/files/{uploaded.filename}"
        else:
            message = "No file selected."

    return render_template("upload_vulnerable.html", message=message, file_url=file_url)


@bp.get("/files/<path:filename>")
def files(filename):
    return send_from_directory(upload_root(), filename)
