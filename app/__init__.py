import flask
import flask_sqlalchemy
import flask_migrate


# Define app
app = flask.Flask(__name__)
# Storage directory
app.config["STORAGE_PATH"] = "/home/stavros/DATA/InfoKiosk"
# Configure SQL SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}/places.db".format(
    app.config["STORAGE_PATH"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Define database
db = flask_sqlalchemy.SQLAlchemy(app)

migrate = flask_migrate.Migrate(app, db)


import os
from app import categories
from app import models


@app.route('/', methods=["GET", "POST"])
def main():
  return flask.render_template("home.html", categories=categories.all)


@app.route("/maps")
def maps():
  image_names = ["base_map.png", "beach_map.png"]
  images = (os.path.join("/static/images", name) for name in image_names)
  return flask.render_template("maps.html", images=images)


@app.route("/places")
def places():
  return flask.render_template("places.html", places=models.Beaches.query.all())
