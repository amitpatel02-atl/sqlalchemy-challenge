from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session= Session(engine)
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
        f"/api/v1.0/precipitation<br/>Returns a JSON list of percipitation data for the dates between 8/23/16 and 8/23/17<br/><br/>"
        f"/api/v1.0/stations<br/>Return a JSON list of stations from the dataset"
        f"/api/v1.0/tobs<br/>Return a JSON list of temperature observations (TOBS) for the previous year."
        f"/api/v1.0/<start><br/>Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given"
        f"/api/v1.0/<start>/<end>Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given"
    )
#########################################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return a list of rain fall for prior year"""
    # Query for the dates and precipitation observations from the last year.
    # Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
    # Return the json representation of your dictionary.
    query_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first() 
    query_date = query_date[0]
    query_date =  dt.datetime.strptime(query_date,'%Y-%m-%d').date()
    start_date_datetime = query_date - dt.timedelta(days=365)
    results= session.query(Measurement.date, Measurement.prcp).\
            filter (Measurement.date >= start_date_datetime).all()
    prcp= {date:prcp for date,prcp in results}
    return jsonify (prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Query station tables
    query_stations = session.query(Station.station).all()
    results = list(np.ravel(query_stations))
    return jsonify (results)

@app.route("/api/v1.0/tobs")
def tobs():
    # Query of dates and temperatures
    query_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first() 
    query_date = query_date[0]
    query_date =  dt.datetime.strptime(query_date,'%Y-%m-%d').date()
    start_date_datetime = query_date - dt.timedelta(days=365)
    query_measure = session.query(Measurement.tobs).\
        filter (Measurement.date >= start_date_datetime).\
        filter ()

    return jsonify ()

if __name__ == '__main__' :
    app.run()  

