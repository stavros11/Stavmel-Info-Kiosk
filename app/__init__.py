import flask

# Define app
app = flask.Flask(__name__)


import os
from app import categories


@app.route('/', methods=["GET", "POST"])
def main():
  return flask.render_template("home.html", categories=categories.all)


@app.route("/maps")
def maps():
  image_names = ["base_map.png", "beach_map.png"]
  images = (os.path.join("/static/images", name) for name in image_names)
  return flask.render_template("maps.html", images=images)
