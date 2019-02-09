from flask import render_template
from . import bp


@bp.route("/")
def home_page():
    username = "233"
    number = 1
    return render_template('content.html', title="Home")