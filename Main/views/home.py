from flask import render_template
from flask import redirect
from . import bp
from . import db
from ..database import Database
from ..methods import check_login_status


@bp.route("/")
def home_page():
    username = check_login_status()
    block_number = db.get_block_amount()
    if block_number > 10:
        block_number = 10
    content = db.get_content(block_number)
    return render_template('home.html', title="Home", username=username, number=block_number, content=content)

@bp.route('/me')
def me():
    username = check_login_status()
    return render_template('me.html', username=username, title="About Me")

@bp.route("/article/<block_id>")
def article(block_id):
    username = check_login_status()
    content = db.select(block_id)
    title = content["title"]
    if content == "001": 
        return redirect("/")
    elif content == "002":
        return redirect("/500")
    else:
        return render_template('article.html', username=username, title=title, content=content)
        
@bp.route("/archive")
def archive():
    pass