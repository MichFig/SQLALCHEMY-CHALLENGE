import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy import create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float 
from flask import Flask, jsonify
from requests.sessions import session
import _datetime as dt

# Database Setup 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Flask Setup
app = Flask(__name__)

# Flask Routes

@app.route("/")
def welcome():
    
    return (
        f"Welcome to Michelle's Surf's Up API<br/>"
        "<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br>"
        f"/api/v1.0/<start>/<end>"
        )

@app.route("/api/v1.0/precipitation") 
def precipitation():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query Measurement prcp
    results = prcp_results = session.query(Measurement.date, Measurement.prcp).\
                   filter(Measurement.date.between('2016-08-23', '2017-08-23')).all()

    # Create a dictionary from the row data and append to a list 
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        all_precip.append(precip_dict)

    return jsonify(all_precip)

@app.route("/api/v1.0/stations") 
def stations():
    # Create session (link) from Python to the DB
    session = Session(engine)

    # Query Stations
    results = session.query(Station.station, Station.name).all()


    # Create a dictionary from the row data and append to a list 
    all_station = []
    for station, name in results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        all_station.append(station_dict)

    return jsonify(all_station)
  
@app.route("/api/v1.0/tobs")
def tobs():
    # Create session (link) from Python to the DB
    session = Session(engine)

    last_data_point = dt.date(2017, 8, 23)
    year_from_last = last_data_point - dt.timedelta(days=365)
    
    # Query Stations
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= year_from_last, Measurement.station =='USC00519281').all()
    
    tobs_list = list(np.ravel(results))

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
def start(start, end=""):
    # Create session (link) from Python to the DB
    session = Session(engine)
   
    # Query Stations
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start).all()

    # Create a dictionary from the row data and append to a list of all_stations
    all_mmat = []
    for mmat in results:
        mmat_dict = {}
        mmat_dict["TMIN"] = mmat[0]
        mmat_dict["TAVG"] = mmat[1]
        mmat_dict["TMAX"] = mmat[2]
        all_mmat.append(mmat_dict)

    return jsonify(all_mmat)

@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
    # Create session (link) from Python to the DB
    session = Session(engine)

   # Query Stations
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs))\
                            .filter(Measurement.date >= start)\
                            .filter(Measurement.date <= end).all()
    
    # Create a dictionary from the row data and append to a list of all_stations
    all_mmat = []
    for mmat in results:
        mmat_dict = {}
        mmat_dict["TMIN"] = mmat[0]
        mmat_dict["TAVG"] = mmat[1]
        mmat_dict["TMAX"] = mmat[2]
        all_mmat.append(mmat_dict)

    return jsonify(all_mmat)
if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1",port=8017)