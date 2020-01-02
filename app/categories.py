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


all = [Category("Transportation", "maps", "transportation.png"),
       Category("Maps", "maps", "map.jpg"),
       Category("Places of Interest", "maps", "poi.png"),
       Category("Weather", "maps", "weather.png"),
       Category("Useful phones", "maps", "phone.png")]
