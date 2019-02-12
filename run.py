from flask import Flask
from Main import app
from Main import database
from Main import db

if __name__ == "__main__":
    app.run(host="127.0.0.1", port = 80, debug=1)
    db.disconnect()
