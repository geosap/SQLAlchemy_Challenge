import datetime as dt
import numpy as np
import pandas as pd

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end"
    )

@app.route("/api/v1.0/precipitation")
# precip link
def precip():
    prev_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precip_12m = session.query(measurement.date, measurement.prcp).filter(measurement.date>=prev_yr).all()
    precip = {date: prcp for date, prcp in precip_12m}
    session.close()
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # station link
    station_list = session.query(station.station).all()
    session.close()
    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # TOB link
    prev_yr = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    tobs_12m = session.query(measurement.tobs).filter(measurement.date>=prev_yr).\
        filter(measurement.station =='USC00519281').all()
    session.close()
    return jsonify(tobs_12m)

@app.route("/api/v1.0/temp/<start>")
def start(start):
    result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).all()
    session.close()
    return jsonify(result)


@app.route("/api/v1.0/temp/<start>/<end>")
def start_end(start,end):
    result = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    print(result)
    session.close()
    return jsonify(result)

# if __name__ == '__main__':
#     app.run(debug=True)