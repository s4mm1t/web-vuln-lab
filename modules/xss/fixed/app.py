from flask import Blueprint, render_template, request


bp = Blueprint(
    "xss_fixed",
    __name__,
    url_prefix="/xss/fixed",
    template_folder="templates",
)


@bp.get("/")
def search():
    query = request.args.get("q", "")
    response = render_template("xss_fixed_search.html", query=query)
    headers = {"Content-Security-Policy": "default-src 'self'; script-src 'self'; object-src 'none'"}
    return response, 200, headers
