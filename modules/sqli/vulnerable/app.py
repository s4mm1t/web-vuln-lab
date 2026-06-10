import sqlite3

from flask import Blueprint, render_template, request


bp = Blueprint(
    "sqli_vulnerable",
    __name__,
    url_prefix="/sqli/vulnerable",
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
    sql = None
    username = "admin"
    password = "wrong"

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        conn = seed_connection()
        try:
            user = conn.execute(sql).fetchone()
        except sqlite3.Error as exc:
            result = f"SQL error: {exc}"
        else:
            result = f"Welcome, {user['username']}!" if user else "Invalid credentials."
        finally:
            conn.close()

    return render_template(
        "sqli_vulnerable_login.html",
        result=result,
        sql=sql,
        username=username,
        password=password,
    )
