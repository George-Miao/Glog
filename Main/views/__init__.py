from flask import Blueprint
from flask import render_template
from ..databaser import Database
from ..methods import get_ip


ip = "10.5.3.234"
bp = Blueprint("bp", __name__,)
db = Database()
db.connect("localhost", "root", "George219@", "mydb")#"localhost", "root", "George219@", "mydb"


from . import editor
from . import home
from . import user
from . import error
