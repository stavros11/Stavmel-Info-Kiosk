import os
import sqlalchemy
import pandas as pd

data_dir = "/home/stavros/DATA/InfoKiosk"


def transform_website(url: str) -> str:
  if not url:
    return url
  if url is None or not isinstance(url, str):
    return None
  return '<a href=http://{} target="blank">{}</a>'.format(url, url)


def transform_ktel_times(times_str: str) -> str:
  if not times_str or not isinstance(times_str, str):
    return None

  transformed_times = []
  for route in times_str.split(" -"):
    elements = route.split(" ")
    if not elements or len(elements) > 3:
      print("Inappropriate time found in KTEL routes {}.".format(times_str))
      _ = input() # Used to stop CMD window from closing on Windows
    elif len(elements) == 1:
      elements.append("00")
      elements.append("")
    elif len(elements) == 2:
      elements.append("")
    transformed_times.append("{}.{}{}".format(*elements))
  return ", ".join(transformed_times)


required_columns = ['name',
                    'opening_hours',
                    'telephone',
                    'fax',
                    'email',
                    'website',
                    'contact',
                    'address',
                    'price',
                    'photo_url',
                    'description',
                    'google_maps',
                    'latitude',
                    'longitude',
                    'directions_url',
                    'road_distance',
                    'road_time']


# Map from csv file names to SQL table names
filenames = {"beaches": "beach",
             "monuments": "monument",
             "natural": "natural",
             "museums": "museum",
             "hospitals": "hospital",
             "info_points": "info",
             "open_markets": "market",
             "walking_routes": "walking"}


if __name__ == "__main__":
  # Remove `data.db` file if it exists
  file_path = os.path.join(data_dir, "data.db")
  if os.path.exists(file_path):
    os.remove(file_path)

  # Define database file
  db_uri = "sqlite:///{}".format(file_path)
  engine = sqlalchemy.create_engine(db_uri, echo=False)

  # Add places to database
  for filename, tablename in filenames.items():
    data = pd.read_csv(os.path.join(data_dir, "{}.csv".format(filename)))
    data["website"] = data["website"].map(transform_website)

    if list(data.columns) != required_columns:
      raise KeyError("{} has incorrect columns.".format(filename))

    sql_database = data.to_sql(tablename, con=engine)


  # Add useful phones to database
  data = pd.read_csv(os.path.join(data_dir, "useful_phones.csv"))
  data["website"] = data["website"].map(transform_website)
  data.to_sql("phone", con=engine)


  # Add taxi prices to database
  data = pd.read_csv(os.path.join(data_dir, "taxi_prices.csv"))
  data.to_sql("taxi", con=engine)


  # Add KTEL routes to database
  data = pd.read_csv(os.path.join(data_dir, "ktel.csv"))
  ktel_columns = ["from_rhodes", "to_rhodes", "from_rhodes_sunday",
                  "to_rhodes_sunday"]
  for k in ktel_columns:
    data[k] = data[k].map(transform_ktel_times)
  data.to_sql("ktel", con=engine)
