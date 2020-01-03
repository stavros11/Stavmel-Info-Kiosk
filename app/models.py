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


class Beaches(db.Model):
  name = db.Column(db.String(128), primary_key=True)
  photo_url = db.Column(db.String(512))
  google_maps = db.Column(db.String(1024))
  description = db.Column(db.String(50000))
  latitude = db.Column(db.Float())
  longitude = db.Column(db.Float())

  @property
  def id(self) -> str:
    return "".join(word.lower() for word in self.name.split(" "))

  @property
  def distance(self) -> float:
    return spherical_earth_projected_distance(self.latitude, self.longitude)
