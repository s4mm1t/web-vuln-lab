from flask import Blueprint, abort, render_template, request, session


bp = Blueprint(
    "idor_fixed",
    __name__,
    url_prefix="/idor/fixed",
    template_folder="templates",
)

PROFILES = {
    1: {"owner_id": 1, "name": "Alice", "email": "alice@example.test", "plan": "Free"},
    2: {"owner_id": 2, "name": "Bob", "email": "bob@example.test", "plan": "Enterprise"},
}


@bp.get("/")
def profile():
    session.setdefault("user_id", 1)
    requested_id = request.args.get("id", str(session["user_id"]))
    try:
        profile_id = int(requested_id)
    except ValueError:
        abort(404)

    profile_data = PROFILES.get(profile_id)
    if not profile_data:
        abort(404)
    if profile_data["owner_id"] != session["user_id"]:
        abort(403)

    return render_template("idor_fixed.html", profile=profile_data, profile_id=profile_id)
