from flask import render_template
from flask import redirect
from flask import request
from flask import make_response
from . import bp
from . import db
from . import ip
from ..database import Database
from ..methods import check_login_status



@bp.route("/login")
def login_page():
    username = check_login_status()
    target = request.args.get("target")
    if target == None:
        target = ""
    if username != "0":
        return redirect("/")
    else:
        return render_template("user_handling/login.html", ip = ip, target = target, title = "Login")

@bp.route("/logout")
def logout():
    resp = make_response(redirect("/"))
    resp.set_cookie('username', '', expires=0)
    return resp

@bp.route("/register")
def register_page():
    return render_template("user_handling/register.html", ip = ip, title="Register")

@bp.route("/login_handling", methods = ['GET', 'POST'])
def login_handling():
    name, passwd = request.form["username"], request.form["password"]
    response = db.login(name, passwd)
    if response == "000":
        response = make_response(response)
        response.set_cookie('username', name, max_age=3600)
    return response

@bp.route("/register_handling", methods = ['GET', 'POST'])
def register_handling():
    name, passwd = request.form["username"], request.form["password"]
    response = db.register(name, passwd)
    response = make_response(response)
    return response