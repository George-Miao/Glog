from flask import Blueprint
from ..database import Database

bp = Blueprint("bp", __name__,)
db = Database()
db.connect()

from . import editor
from . import home
from . import user
from . import error
