import os
import flask


class Category:
  """Objects that appear in the home page."""

  def __init__(self, name: str, url: str, photo: str, new_tab: bool = False):
    self.name = name
    self.url_name = url
    self.photo = os.path.join("/static/images", photo)
    self.new_tab = new_tab

  @property
  def url(self):
    return flask.url_for(self.url_name)


class CategoryWeather:

  def __init__(self):
    self.name = "Weather"
    self.photo = os.path.join("/static/images", "weather.png")
    self.new_tab = True
    self.url = "https://weather.com/weather/today/l/f0de8849c0ac9f287c8d68536eb02828142419816360f365c396c7c9782f6819"


main = [Category("Transportation", "maps", "transportation.png"),
        Category("Maps", "maps", "map.jpg"),
        Category("Places of Interest", "places", "poi.png"),
        CategoryWeather(),
        Category("Useful phones", "phones", "phone.png")]


class PlaceCategory(Category):

  @property
  def url(self):
    return flask.url_for("places_list", place_type=self.url_name)


places = [PlaceCategory("Beaches", "Beach", "beaches.jpg"),
          PlaceCategory("Monuments", "Monument", "monuments.jpg"),
          PlaceCategory("Museums", "Museum", "museum.jpg"),
          PlaceCategory("Areas of Natural Beauty", "Natural", "natural.jpg")]
