from .views import bp
from flask import Flask


app = Flask(__name__)
app.register_blueprint(bp)


@app.route("/")
def home_page():
    return "..."
