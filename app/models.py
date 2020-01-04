import numpy as np
from app import db


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
  photo_url = db.Column(db.String(512))
  description = db.Column(db.String(50000))
  google_maps = db.Column(db.String(1024))
  directions_url = db.Column(db.String(4096))
  road_distance = db.Column(db.Float())
  road_time = db.Column(db.Float())
  latitude = db.Column(db.Float())
  longitude = db.Column(db.Float())

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


class BaseSight(BasePlace):
  opening_hours = db.Column(db.String(128))
  telephone = db.Column(db.String(128))
  address = db.Column(db.String(128))
  price = db.Column(db.String(128))


class Beach(db.Model, BasePlace): pass
class Museum(db.Model, BaseSight): pass
class Monument(db.Model, BaseSight): pass
class Natural(db.Model, BaseSight): pass
