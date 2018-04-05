import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

today = str(dt.datetime.today().year)+"-"+str(dt.datetime.today().month)+"-"+str(dt.datetime.today().day)

def calc_temps(trip_start_date,trip_end_date=today):
    
    minimum = session.query(func.min(Measurement.tobs)).\
    filter(Measurement.date > trip_start_date, Measurement.date < trip_end_date)\
    [0][0]

    if minimum == None:
        print("Trip needs to be longer, exiting")
        return("trip needs to be longer OR date needs the following format: yyyy-mm-dd")

    average = round(session.query(func.avg(Measurement.tobs)).\
    filter(Measurement.date > trip_start_date, Measurement.date < trip_end_date)\
    [0][0],2)
    
    maximum = session.query(func.max(Measurement.tobs)).\
    filter(Measurement.date > trip_start_date, Measurement.date < trip_end_date)\
    [0][0]

#     return "minimum = " + str(minimum) + ", " + "maximum = " + str(maximum) + ", " + "average = " + str(average)
    return minimum, average, maximum


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Stations = Base.classes.stations

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/<start>'>/api/v1.0/&lt;start &gt;</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>/api/v1.0/&lt;start &gt;/&lt;end &gt;</a>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year = dt.date.today() - dt.timedelta(days=365)

    query = session.query(Measurement).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()

    precipitation = []
    for instance in query:
        precipitation_dict = {}
        precipitation_dict["date"] = instance.date
        precipitation_dict["tobs"] = instance.tobs
        precipitation.append(precipitation_dict)

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    query = session.query(Stations.name).all()

    station_names = list(np.ravel(query))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year = dt.date.today() - dt.timedelta(days=365)

    last_year_tobs = session.query(Measurement).\
        filter(Measurement.date > last_year).\
        order_by(Measurement.date).all()
    
    tobs = [result.tobs for result in last_year_tobs]

    return jsonify(tobs)

@app.route("/api/v1.0/<string:start>")
def start(start):
    
    results = calc_temps(start)

    return jsonify(results)

@app.route("/api/v1.0/<string:start>/<string:end>")
def start_end(start, end):    

    results = calc_temps(start,end)
    
    return jsonify(results)




if __name__ == '__main__':
    app.run(debug=True)
