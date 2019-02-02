from flask import Blueprint, render_template

profile = Blueprint('profile', __name__)

@app.route('/')
def home():
    number = bid(limit=True)
    content = generate(number)
    return render_template('content.html', number=number, title="Home", content=content)