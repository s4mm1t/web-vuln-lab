from pathlib import Path
import html
import re

from flask import Flask, abort, render_template
from markupsafe import Markup


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


def render_inline_markdown(text):
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def render_markdown(markdown):
    html_parts = []
    in_code = False
    in_list = False
    in_section = False
    code_lines = []
    code_lang = ""

    def close_list():
        nonlocal in_list
        if in_list:
            html_parts.append("</ul>")
            in_list = False

    def close_section():
        nonlocal in_section
        close_list()
        if in_section:
            html_parts.append("</section>")
            in_section = False

    for raw_line in markdown.splitlines():
        line = raw_line.rstrip()

        if line.startswith("```"):
            if in_code:
                escaped_code = html.escape("\n".join(code_lines))
                html_parts.append(
                    f'<pre class="writeup-code" data-lang="{html.escape(code_lang)}"><code>{escaped_code}</code></pre>'
                )
                in_code = False
                code_lines = []
                code_lang = ""
            else:
                close_list()
                in_code = True
                code_lang = line.strip("`").strip() or "text"
            continue

        if in_code:
            code_lines.append(line)
            continue

        if not line.strip():
            close_list()
            continue

        if line.startswith("# "):
            close_section()
            title = render_inline_markdown(line[2:].strip())
            html_parts.append(f'<header class="writeup-hero"><p class="eyebrow">Case writeup</p><h1>{title}</h1></header>')
            continue

        if line.startswith("## "):
            close_section()
            title = render_inline_markdown(line[3:].strip())
            html_parts.append(f'<section class="writeup-section"><h2>{title}</h2>')
            in_section = True
            continue

        if line.startswith("- "):
            if not in_list:
                html_parts.append('<ul class="writeup-list">')
                in_list = True
            item = render_inline_markdown(line[2:].strip())
            html_parts.append(f"<li>{item}</li>")
            continue

        close_list()
        paragraph = render_inline_markdown(line)
        html_parts.append(f"<p>{paragraph}</p>")

    if in_code:
        escaped_code = html.escape("\n".join(code_lines))
        html_parts.append(f'<pre class="writeup-code" data-lang="{html.escape(code_lang)}"><code>{escaped_code}</code></pre>')
    close_section()
    return Markup("\n".join(html_parts))


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
        module = next((module for module in MODULES if module["key"] == module_key), None)
        if module is None:
            abort(404)

        path = Path(app.root_path).parent / "modules" / module_key / "writeup.md"
        if not path.exists():
            abort(404)

        content = path.read_text(encoding="utf-8")
        return render_template(
            "writeup.html",
            content=render_markdown(content),
            module=module,
            title=f"{module['name']} Writeup",
        )

    return app


app = create_app()
