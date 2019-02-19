from . import bp
from flask import render_template

@bp.route("/404")
def page_404():
    return render_template("error.html", title="404")


@bp.route("/500")
def page_500():
    return render_template("error.html", title="500")