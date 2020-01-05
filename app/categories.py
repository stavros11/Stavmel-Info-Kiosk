import os
import flask


class Category:
  """Objects that appear in the home page."""

  def __init__(self, name: str, url: str, photo: str, new_tab: bool = False):
    self.name = name
    self._url = url
    self.photo = os.path.join("/static/images", photo)
    self.new_tab = new_tab

  @property
  def url(self):
    return flask.url_for(self._url)


class CategoryURL(Category):

  @property
  def url(self):
    return self._url


class PlaceCategory(Category):

  @property
  def url(self):
    return flask.url_for("places_list", place_type=self._url)


weather_url = "https://weather.com/weather/today/l/f0de8849c0ac9f287c8d68536eb02828142419816360f365c396c7c9782f6819"
main = [Category("Transportation", "maps", "transportation.png"),
        Category("Maps", "maps", "map.jpg"),
        Category("Places of Interest", "places", "poi.png"),
        CategoryURL("Weather", weather_url, "weather.png", new_tab=True),
        Category("Useful phones", "phones", "phone.png")]


water_park_url = "https://www.water-park.gr/"
places = [PlaceCategory("Beaches", "Beach", "beaches.jpg"),
          PlaceCategory("Monuments", "Monument", "monuments.jpg"),
          PlaceCategory("Museums", "Museum", "museum.jpg"),
          PlaceCategory("Areas of Natural Beauty", "Natural", "natural.jpg"),
          CategoryURL("Water Park", water_park_url, "waterpark.png", new_tab=True)]
