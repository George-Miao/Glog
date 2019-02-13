from flask import render_template
from flask import redirect
from . import bp
from . import db
from ..database import Database
from ..methods import check_login_status


@bp.route("/")
def home_page():
    username = check_login_status()
    block_number = db.get_block_id()
    content = db.generate_content(block_number)
    return render_template('content.html', title="Home", username=username, number=block_number, content=content)

@bp.route('/me')
def me():
    username = check_login_status()
    return render_template('me.html', username=username, title="About Me")

@bp.route("/article/<block_id>")
def article(block_id):
    title = block_id
    content = db.generate_content(block_id, is_detailed=True)
    if content == "000": 
        return redirect("/")
    else:
        return render_template('article.html', title = title, content = content)