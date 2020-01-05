import os
import sqlalchemy
import pandas as pd

data_dir = "/home/stavros/DATA/InfoKiosk"

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
             "hospitals": "hospital"}


# Define database file
db_uri = "sqlite:///{}/data.db".format(data_dir)
engine = sqlalchemy.create_engine(db_uri, echo=False)

# Add places to database
for filename, tablename in filenames.items():
  data = pd.read_csv(os.path.join(data_dir, "{}.csv".format(filename)))
  if list(data.columns) != required_columns:
    raise KeyError("{} has incorrect columns.".format(filename))

  sql_database = data.to_sql(tablename, con=engine)


# Add useful phones to database
data = pd.read_csv(os.path.join(data_dir, "useful_phones.csv"))
data.to_sql("phone", con=engine)
