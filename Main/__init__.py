from .views import bp
from .views import db
from flask import Flask
from flask import redirect

app = Flask(__name__)
app.register_blueprint(bp)


@app.errorhandler(404)
def e_404(e):
    return redirect("/404")


@app.errorhandler(500)
def e_500(e):
    return redirect("/500")

