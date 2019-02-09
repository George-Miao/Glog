from . import bp


@bp.route("/admin")
def admin_page():
    return "..."