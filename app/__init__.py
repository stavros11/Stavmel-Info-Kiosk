import flask

# Define app
app = flask.Flask(__name__)



from app import categories


@app.route('/', methods=["GET", "POST"])
def main():
  return flask.render_template("home.html", categories=categories.all)


@app.route("/maps")
def maps():
  return flask.redirect(flask.url_for("main"))
