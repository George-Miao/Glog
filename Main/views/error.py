from . import bp
from flask import render_template

@bp.errorhandler(404)
@bp.route("/404")
def e_404(e):
    return render_template("error.html", title="404")


@bp.errorhandler(500)
@bp.route("/500")
def e_500(e):
    return render_template("error.html", title="500")