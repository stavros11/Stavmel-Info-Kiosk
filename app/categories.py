import os
import flask


class Category:
  """Objects that appear in the home page."""

  def __init__(self, name: str, url: str, photo: str):
    self.name = name
    self.url_name = url
    self.photo = os.path.join("/static/images", photo)

  @property
  def url(self):
    return flask.url_for(self.url_name)


main = [Category("Transportation", "maps", "transportation.png"),
        Category("Maps", "maps", "map.jpg"),
        Category("Places of Interest", "places", "poi.png"),
        Category("Weather", "weather", "weather.png"),
        Category("Useful phones", "maps", "phone.png")]


class PlaceCategory(Category):

  @property
  def url(self):
    return flask.url_for("places_list", place_type=self.url_name)


places = [PlaceCategory("Beaches", "Beach", "beaches.jpg"),
          PlaceCategory("Monuments", "Monument", "monuments.jpg"),
          PlaceCategory("Museums", "Museum", "museum.jpg"),
          PlaceCategory("Areas of Natural Beauty", "Natural", "natural.jpg")]
