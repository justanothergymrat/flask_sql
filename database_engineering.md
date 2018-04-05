

```python
!rm hawaii.sqlite

# Python SQL toolkit and Object Relational Mapper
import pandas as pd
import numpy as np
import os
import sqlalchemy
from datetime import datetime
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, Text, Float, Date
```

Use the engine and connection string to create a database called hawaii.sqlite.

Use declarative_base and create ORM classes for each table.

You will need a class for Measurement and for Station.

Make sure to define your primary keys.

Once you have your ORM classes defined, create the tables in the database using create_all.


```python
# Create engine 
engine = create_engine('sqlite:///hawaii.sqlite', echo=False)

conn = engine.connect()
Base = declarative_base()

# Create classes

class Measurement(Base):
    __tablename__ = 'measurement'

    id = Column(Integer, primary_key=True)
    station = Column(Text)
    date = Column(Date)
    prcp = Column(Float)
    tobs = Column(Integer)

#     def __repr__(self):
#         return f"id={self.id}, name={self.name}"
    
class Stations(Base):
    __tablename__ = 'stations'

    id = Column(Integer, primary_key=True)
    station = Column(Text)
    name = Column(Text)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)

#     def __repr__(self):
#         return f"id={self.id}, name={self.name}"
    
# Create table
Base.metadata.create_all(engine)

```

Use Pandas to read your cleaned measurements and stations CSV data:


```python
#Populate Measurement Table

measurements_clean = "clean_measurements.csv"

# load cleaned data to df
measurement_df = pd.read_csv(measurements_clean)

# convert date to something sqlalchemy likes
measurement_df['date'] = pd.to_datetime(measurement_df['date'])

# get data into tables
data = measurement_df.to_dict(orient='records')
metadata = MetaData(bind=engine)
metadata.reflect()
table1 = sqlalchemy.Table('measurement', metadata, autoload=True)

# push it into DB & verify
conn.execute(table1.delete())
conn.execute(table1.insert(),data)
conn.execute("select * from measurement limit 5").fetchall()
```




    [(1, 'USC00519397', '2010-01-01', 0.08, 65),
     (2, 'USC00519397', '2010-01-02', 0.0, 63),
     (3, 'USC00519397', '2010-01-03', 0.0, 74),
     (4, 'USC00519397', '2010-01-04', 0.0, 76),
     (5, 'USC00519397', '2010-01-07', 0.06, 70)]




```python
#Populate Stations Table

stations_clean = "clean_stations.csv"

# load cleaned data to df
stations_df = pd.read_csv(stations_clean)

# get data into tables
data = stations_df.to_dict(orient='records')
metadata = MetaData(bind=engine)
metadata.reflect()
table2 = sqlalchemy.Table('stations', metadata, autoload=True)

# push it into DB & verify
conn.execute(table2.delete())
conn.execute(table2.insert(),data)
conn.execute("select * from stations").fetchall()
```




    [(1, 'USC00519397', 'WAIKIKI 717.2, HI US', 21.2716, -157.8168, 3.0),
     (2, 'USC00513117', 'KANEOHE 838.1, HI US', 21.4234, -157.8015, 14.6),
     (3, 'USC00514830', 'KUALOA RANCH HEADQUARTERS 886.9, HI US', 21.5213, -157.8374, 7.0),
     (4, 'USC00517948', 'PEARL CITY, HI US', 21.3934, -157.9751, 11.9),
     (5, 'USC00518838', 'UPPER WAHIAWA 874.3, HI US', 21.4992, -158.0111, 306.6),
     (6, 'USC00519523', 'WAIMANALO EXPERIMENTAL FARM, HI US', 21.33556, -157.71139, 19.5),
     (7, 'USC00519281', 'WAIHEE 837.5, HI US', 21.45167, -157.84888999999995, 32.9),
     (8, 'USC00511918', 'HONOLULU OBSERVATORY 702.2, HI US', 21.3152, -157.9992, 0.9),
     (9, 'USC00516128', 'MANOA LYON ARBO 785.2, HI US', 21.3331, -157.8025, 152.4)]


