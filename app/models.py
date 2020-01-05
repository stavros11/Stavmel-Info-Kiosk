import os
import flask
import numpy as np
from app import db


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


def spherical_earth_projected_distance(latitude: float,
                                       longitude: float,
                                       latitude0: float = 36.398010,
                                       longitude0: float = 28.228522,
                                       radius: float = 6371):
  dphi = (latitude - latitude0) * np.pi / 180.0
  phi_m = (latitude + latitude0) * np.pi / 360.0
  dlambda = (longitude - longitude0) * np.pi / 180.0
  d2 = dphi**2 + (np.cos(phi_m) * dlambda)**2
  return radius * np.sqrt(d2)


class BasePlace:
  name = db.Column(db.String(128), primary_key=True)
  opening_hours = db.Column(db.String(128))
  telephone = db.Column(db.String(128))
  fax = db.Column(db.String(128))
  email = db.Column(db.String(128))
  website = db.Column(db.String(128))
  contact = db.Column(db.String(128))
  address = db.Column(db.String(128))
  price = db.Column(db.String(128))
  photo_url = db.Column(db.String(512))
  description = db.Column(db.String(50000))
  google_maps = db.Column(db.String(1024))
  latitude = db.Column(db.Float())
  longitude = db.Column(db.Float())
  directions_url = db.Column(db.String(4096))
  road_distance = db.Column(db.Float())
  road_time = db.Column(db.Float())

  # TODO: (OPTIONAL) Fix automatic photo rescaling using the photo size
  #photo_rescale_factor = 0.3
  photo_height = 350
  photo_width = 520

  @property
  def id(self) -> str:
    return "".join(word.lower() for word in self.name.split(" "))

  @property
  def geo_distance(self) -> float:
    if self.latitude is None or self.longitude is None:
      return None
    return spherical_earth_projected_distance(self.latitude, self.longitude)

  @property
  def rounded_geo_distance(self) -> int:
    d = self.geo_distance
    if d is None:
      return d
    return int(round(self.geo_distance))

  @property
  def has_photo(self) -> bool:
    return self.photo_url is not None


class Beach(db.Model, BasePlace): pass
class Museum(db.Model, BasePlace): pass
class Hospital(db.Model, BasePlace): pass
class Info(db.Model, BasePlace): pass


class Monument(db.Model, BasePlace):
  photo_height = 200
  photo_width = 340


class Natural(db.Model, BasePlace):
  photo_height = 280
  photo_width = 400


class Phone(db.Model):
  name = db.Column(db.String(128), primary_key=True)
  telephone = db.Column(db.String(128))
  fax = db.Column(db.String(128))
  email = db.Column(db.String(128))
  website = db.Column(db.String(128))
  address = db.Column(db.String(256))
  contact = db.Column(db.String(128))
  hours = db.Column(db.String(128))
  type = db.Column(db.String(128))
