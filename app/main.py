from pathlib import Path

from flask import Flask, abort, render_template, Response


MODULES = [
    {
        "key": "sqli",
        "name": "SQL Injection",
        "topic": "Parameterized queries",
        "description": "Login form that contrasts string-built SQL with bound parameters.",
    },
    {
        "key": "xss",
        "name": "XSS",
        "topic": "Output escaping and CSP",
        "description": "Reflected search page that shows why unescaped HTML is dangerous.",
    },
    {
        "key": "upload",
        "name": "File Upload",
        "topic": "File validation",
        "description": "Upload flow with unsafe public storage versus strict validation.",
    },
    {
        "key": "auth",
        "name": "Broken Auth",
        "topic": "Sessions and password hashing",
        "description": "GET-based plaintext login versus POST, bcrypt, and hardened cookies.",
    },
    {
        "key": "idor",
        "name": "IDOR",
        "topic": "Object authorization",
        "description": "Profile lookup that demonstrates missing ownership checks.",
    },
]


def create_app(test_config=None):
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_mapping(
        SECRET_KEY="dev-only-change-me",
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        MAX_CONTENT_LENGTH=1 * 1024 * 1024,
    )

    if test_config:
        app.config.update(test_config)

    from modules.auth.fixed.app import bp as auth_fixed_bp
    from modules.auth.vulnerable.app import bp as auth_vulnerable_bp
    from modules.idor.fixed.app import bp as idor_fixed_bp
    from modules.idor.vulnerable.app import bp as idor_vulnerable_bp
    from modules.sqli.fixed.app import bp as sqli_fixed_bp
    from modules.sqli.vulnerable.app import bp as sqli_vulnerable_bp
    from modules.upload.fixed.app import bp as upload_fixed_bp
    from modules.upload.vulnerable.app import bp as upload_vulnerable_bp
    from modules.xss.fixed.app import bp as xss_fixed_bp
    from modules.xss.vulnerable.app import bp as xss_vulnerable_bp

    for bp in [
        sqli_vulnerable_bp,
        sqli_fixed_bp,
        xss_vulnerable_bp,
        xss_fixed_bp,
        upload_vulnerable_bp,
        upload_fixed_bp,
        auth_vulnerable_bp,
        auth_fixed_bp,
        idor_vulnerable_bp,
        idor_fixed_bp,
    ]:
        app.register_blueprint(bp)

    @app.get("/")
    def index():
        return render_template("index.html", modules=MODULES)

    @app.get("/writeups/<module_key>")
    def writeup(module_key):
        allowed = {module["key"] for module in MODULES}
        if module_key not in allowed:
            abort(404)

        path = Path(app.root_path).parent / "modules" / module_key / "writeup.md"
        if not path.exists():
            abort(404)

        content = path.read_text(encoding="utf-8")
        return Response(content, mimetype="text/markdown; charset=utf-8")

    return app


app = create_app()
