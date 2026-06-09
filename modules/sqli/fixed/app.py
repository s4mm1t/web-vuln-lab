import sqlite3

from flask import Blueprint, render_template, request


bp = Blueprint(
    "sqli_fixed",
    __name__,
    url_prefix="/sqli/fixed",
    template_folder="templates",
)


def seed_connection():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    conn.executemany(
        "INSERT INTO users (username, password) VALUES (?, ?)",
        [("admin", "password123"), ("alice", "wonderland")],
    )
    return conn


@bp.route("/", methods=["GET", "POST"])
def login():
    result = None
    query = "SELECT * FROM users WHERE username = ? AND password = ?"

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = seed_connection()
        user = conn.execute(query, (username, password)).fetchone()
        conn.close()
        result = f"Welcome, {user['username']}!" if user else "Invalid credentials."

    return render_template("sqli_fixed_login.html", result=result, query=query)
