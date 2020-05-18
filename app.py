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
engine = create_engine("sqlite:///Resources/hawaii.sqlite")")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/precipitation:<br/>Returns a JSON list of percipitation data for the dates between 8/23/16 and 8/23/17<br/><br/>"
        f"/api/v1.0/stations:<br/>Return a JSON list of stations from the dataset"
        f"/api/v1.0/tobs:<br/>Return a JSON list of temperature observations (TOBS) for the previous year."
        f"/api/v1.0/<start>:<br/>Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given           f"start or start-end range."
        f"/api/v1.0/<start>/<end>Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given           f"start or start-end range."
    )
#########################################################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
        """Return a list of rain fall for prior year"""
#    * Query for the dates and precipitation observations from the last year.
#           * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
#           * Return the json representation of your dictionary.
query_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first() 
start_date_datetime = end_date_datetime - dt.timedelta(days=365)
