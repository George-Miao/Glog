from flask import Blueprint
from ..database import Database
from ..methods import get_ip

ip = get_ip()
bp = Blueprint("bp", __name__,)
db = Database()
db.connect()

from . import editor
from . import home
from . import user
from . import error
