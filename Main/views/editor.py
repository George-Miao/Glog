from . import bp
from . import db
from . import ip
from ..database import Database
from ..methods import check_login_status
from flask import redirect
from flask import render_template
from flask import request
import datetime
import json


@bp.route("/editor")
def admin_page():
    username = check_login_status()
    if username == "001":
        return redirect("/login?target=editor")
    elif username == "admin":
        number = db.get_block_amount()
        content = db.get_content(number)
        return render_template("editor.html", ip = ip, title="Editor", number=number,  content=content)
    else:
        return redirect("/")

@bp.route("/save", methods=['GET', 'POST'])
def save():
    content = request.form.to_dict()
    content["edit_time"] = datetime.datetime.now()
    return db.edit(content)
    

@bp.route("/create", methods=['GET', 'POST'])
def new():
    title = request.form["title"]
    content = request.form["content"]
    if title == "":
        title = "New post"
    bid = db.create(title, content)
    return bid


@bp.route("/fetch", methods=['GET', 'POST'])
def fetch():
    bid = request.form["id"]
    results = db.select(bid)
    return json.dumps(results)


@bp.route("/delete", methods=['GET', 'POST'])
def d():
    bid = request.form["id"]
    db.delete(bid)
    return "1"
    
