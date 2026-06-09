from flask import Blueprint, render_template, request, session


bp = Blueprint(
    "idor_vulnerable",
    __name__,
    url_prefix="/idor/vulnerable",
    template_folder="templates",
)

PROFILES = {
    1: {"owner_id": 1, "name": "Alice", "email": "alice@example.test", "plan": "Free"},
    2: {"owner_id": 2, "name": "Bob", "email": "bob@example.test", "plan": "Enterprise"},
}


@bp.get("/")
def profile():
    session.setdefault("user_id", 1)
    requested_id = request.args.get("id", "1")
    try:
        profile_id = int(requested_id)
    except ValueError:
        profile_id = 1

    profile_data = PROFILES.get(profile_id)
    return render_template(
        "idor_vulnerable.html",
        profile=profile_data,
        profile_id=profile_id,
        current_user_id=session["user_id"],
    )
