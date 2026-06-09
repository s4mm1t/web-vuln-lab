from flask import Blueprint, render_template, request


bp = Blueprint(
    "auth_vulnerable",
    __name__,
    url_prefix="/auth/vulnerable",
    template_folder="templates",
)

USERS = {"admin": "123456", "alice": "password"}


@bp.get("/")
def login_form():
    username = request.args.get("username", "")
    password = request.args.get("password", "")
    message = None

    if username or password:
        if USERS.get(username) == password:
            message = f"Logged in as {username}, but no real server-side session was created."
        else:
            message = "Invalid credentials."

    return render_template(
        "auth_vulnerable.html",
        username=username,
        password=password,
        message=message,
    )
