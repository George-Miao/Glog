from .views import bp
from .views import db
from flask import Flask


app = Flask(__name__)
app.register_blueprint(bp)


