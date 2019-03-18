import os

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'db.plantpal')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Init Database
db = SQLAlchemy(app)

# Init Marshmallow
marshmallow = Marshmallow(app)

DEBUG = True
PORT = 8000


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route('/signup')
def signup():
    return render_template("signup.html")


@app.route('/profile/')
@app.route("/profile/<username>", methods=["GET", "POST", "DELETE"])
def profile(username=None):
    if username == None:
        return render_template("login.html")
    else:
        return render_template("profile.html", username=username)


@app.route('/plants/')
def plants():
    return render_template('plants.html')


if __name__ == '__main__':
    app.run(debug=DEBUG, port=PORT)
