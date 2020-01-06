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
