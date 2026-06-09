import bcrypt

from flask import Blueprint, redirect, render_template, request, session, url_for


bp = Blueprint(
    "auth_fixed",
    __name__,
    url_prefix="/auth/fixed",
    template_folder="templates",
)

PASSWORD_HASH = bcrypt.hashpw(b"password123", bcrypt.gensalt(rounds=12))
USERS = {
    "admin": {
        "id": 1,
        "username": "admin",
        "password_hash": PASSWORD_HASH,
    }
}


@bp.route("/", methods=["GET", "POST"])
def login():
    message = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "").encode("utf-8")
        user = USERS.get(username)

        if user and bcrypt.checkpw(password, user["password_hash"]):
            session.clear()
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            return redirect(url_for("auth_fixed.profile"))

        message = "Invalid credentials."

    return render_template("auth_fixed.html", message=message)


@bp.get("/profile")
def profile():
    if "user_id" not in session:
        return redirect(url_for("auth_fixed.login"))
    return render_template("auth_fixed_profile.html", username=session["username"])


@bp.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth_fixed.login"))
