from flask import Flask
from Main import app


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug = 1)
