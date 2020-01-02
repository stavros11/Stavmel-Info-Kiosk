import flask


# Define app
app = flask.Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def main():
  return flask.render_template("home.html")
