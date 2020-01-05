import flask
import flask_sqlalchemy
import flask_migrate


# Define app
app = flask.Flask(__name__)
# Storage directory
app.config["STORAGE_PATH"] = "/home/stavros/DATA/InfoKiosk"
# Configure SQL SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}/data.db".format(
    app.config["STORAGE_PATH"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Define database
db = flask_sqlalchemy.SQLAlchemy(app)

migrate = flask_migrate.Migrate(app, db)


import os
from app import models


@app.route('/')
def main():
  weather_url = "https://weather.com/weather/today/l/f0de8849c0ac9f287c8d68536eb02828142419816360f365c396c7c9782f6819"
  cats = [models.Category("Transportation", "transportation", "transportation.png"),
          models.Category("Maps", "maps", "map.jpg"),
          models.Category("Places of Interest", "places", "poi.png"),
          models.CategoryURL("Weather", weather_url, "weather.png", new_tab=True),
          models.Category("Emergency", "emergency", "hospital.png"),
          models.Category("Useful phones", "phones", "phone.png")]
  return flask.render_template("home.html", categories=cats,
                               show_home_button=False)


@app.route("/transportation")
def transportation():
  return flask.redirect(flask.url_for("main"))


@app.route("/maps")
def maps():
  image_names = ["base_map.png", "beach_map.png"]
  images = (os.path.join("/static/images", name) for name in image_names)
  return flask.render_template("maps.html", images=images)


@app.route("/places")
def places():
  water_park_url = "https://www.water-park.gr/"
  cats = [models.PlaceCategory("Beaches", "Beach", "beaches.jpg"),
          models.PlaceCategory("Monuments", "Monument", "monuments.jpg"),
          models.PlaceCategory("Museums", "Museum", "museum.jpg"),
          models.PlaceCategory("Areas of Natural Beauty", "Natural", "natural.jpg"),
          models.CategoryURL("Water Park", water_park_url, "waterpark.png", new_tab=True),
          models.PlaceCategory("Tourist Information Offices", "Info", "info.png")]
  return flask.render_template("home.html", categories=cats,
                               show_home_button=True)


@app.route("/places/<place_type>")
def places_list(place_type: str):
  model = getattr(models, place_type)
  data = (model.query.filter(model.road_distance != None).
          order_by(model.road_distance))
  return flask.render_template("places.html", places=data)


@app.route("/emergency")
def emergency():
  data = models.Hospital.query.all()
  return flask.render_template("emergency.html", places=data)


@app.route("/phones")
def phones():
  model = models.Phone
  types_list = ["emergency", "services", "hospitals", "tourism", "consulate"]
  service_types = [(stype.capitalize(), model.query.filter(model.type == stype))
                   for stype in types_list]

  return flask.render_template("phones.html", service_types=service_types)
