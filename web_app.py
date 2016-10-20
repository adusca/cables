import logging
import os

from flask import Flask, request, jsonify, redirect, abort, session, render_template

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s:\t %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S')

app = Flask(__name__)
app.secret_key = os.environ.get("CABLE_KEY")
app.config["SESSION_TYPE"] = "filesystem"
PORT = 8080
DOMAIN = 'localhost:%d' % PORT


@app.route("/")
def index():
    return render_template('index.html')


# For running locally without gunicorn
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
