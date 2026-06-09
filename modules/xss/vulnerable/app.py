from flask import Blueprint, render_template, request


bp = Blueprint(
    "xss_vulnerable",
    __name__,
    url_prefix="/xss/vulnerable",
    template_folder="templates",
)


@bp.get("/")
def search():
    query = request.args.get("q", "")
    return render_template("xss_vulnerable_search.html", query=query)
