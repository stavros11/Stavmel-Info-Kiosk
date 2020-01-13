import os
import json
import flask
import flask_sqlalchemy
import flask_migrate


# Define app
app = flask.Flask(__name__)
# Storage directory
app.config["STORAGE_PATH"] = os.path.join(os.getenv("USERPROFILE"),
                                          "Documents", "info-kiosk-data")
#app.config["STORAGE_PATH"] = "/home/stavros/DATA/InfoKiosk"
# Load predefined urls
with open(os.path.join(app.config["STORAGE_PATH"], "urls.txt")) as file:
  urls_dict = json.load(file)
for url_key, url in urls_dict.items():
  app.config["_".join([url_key, "URL"])] = url
# Configure SQL SQLAlchemy
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///{}/data.db".format(
    app.config["STORAGE_PATH"])
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# Define database
db = flask_sqlalchemy.SQLAlchemy(app)

migrate = flask_migrate.Migrate(app, db)


from app import models


@app.route('/')
def main():
  cats = [models.Category("Transportation", "transportation", "transportation.png"),
          models.Category("Maps", "maps", "map.jpg"),
          models.Category("Places of Interest", "places", "poi.png"),
          models.CategoryURL("Weather", app.config["WEATHER_URL"],
                             "weather.png", new_tab=True),
          models.Category("Emergency", "emergency", "hospital.png"),
          models.Category("Useful phones", "phones", "phone.png")]
  return flask.render_template("home.html", categories=cats,
                               show_home_button=False, page_title="Home")


@app.route("/transportation")
def transportation():
  return flask.render_template("transportation.html")


@app.route("/transportation/taxi")
def taxi():
  return flask.render_template("taxi.html", places=models.Taxi.query.all())


@app.route("/transportation/bus/ktel")
def ktel():
  return flask.render_template("ktel.html", routes=models.Ktel.query.all())


@app.route("/maps")
def maps():
  image_names = ["base_map.png", "beach_map.png"]
  images = (os.path.join("/static/images", name) for name in image_names)
  return flask.render_template("maps.html", images=images)


@app.route("/places")
def places():
  cats = [models.PlaceCategory("Beaches", "Beach", "beaches.jpg"),
          models.PlaceCategory("Monuments", "Monument", "monuments.jpg"),
          models.PlaceCategory("Museums", "Museum", "museum.jpg"),
          models.PlaceCategory("Areas of Natural Beauty", "Natural", "natural.jpg"),
          models.PlaceCategory("Οpen Αir Μarkets", "Market", "market.jpeg"),
          models.PlaceCategory("Walking Routes", "Walking", "walking.jpg"),
          models.PlaceCategory("Tourist Information Offices", "Info", "info.png"),
          models.CategoryURL("Water Park", app.config["WATER_PARK_URL"],
                             "waterpark.png", new_tab=True),
          models.CategoryURL("Throne of Helios", app.config["THRONE_OF_HELIOS_URL"],
                             "throne.jpg", new_tab=True)]
  return flask.render_template("home.html", categories=cats,
                               show_home_button=True, page_title="Places")


@app.route("/places/<place_type>")
def places_list(place_type: str):
  if place_type == "Market":
    return flask.render_template("market.html", places=models.Market.query.all())

  model = getattr(models, place_type)
  data = (model.query.filter(model.road_distance != None).
          order_by(model.road_distance))
  return flask.render_template("places.html", places=data,
                               page_title=place_type.capitalize())


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
