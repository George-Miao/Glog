from flask import Blueprint

bp = Blueprint("bp", __name__)

from . import admin
from . import home
from . import user
