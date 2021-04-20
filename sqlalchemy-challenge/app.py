# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func

import datetime as dt 
from datetime import date

import pandas as pd

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
      f"Hawaii Climate App<br/>"
      f"Available Routes:<br/>"
      f"/api/v1.0/precipitation<br/>"
      f"/api/v1.0/stations<br/>"
      f"/api/v1.0/tobs<br/>"
      f"/api/v1.0/start<br/>"
      f"/api/v1.0/start/end"
      )

@app.route("/api/v1.0/precipitation")
def precip():
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).\
      order_by(Measurement.date).all()
    prcp_data = dict(precipitation)
    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    all_stations = session.query(Station.station, Station.name).all()
    list_stations = list(all_stations)
    return jsonify(list_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobsx = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= one_year_ago).\
      order_by(Measurement.date).all()
    tobs_list = list(tobsx)
    return jsonify(tobs_list)

@app.route("/api/v1.0/start")    
def start_day():
    start_date = dt.date(2017,2,1)
    stats = session.query(Measurement.date, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
      filter(Measurement.date >= start_date).group_by(Measurement.date).all()
    start_list = list(stats)
    return jsonify(start_list)

@app.route("/api/v1.0/start/end")
def start_end_date():
    start_date = dt.date(2017,2,1)
    end_date = dt.date(2017,5,1)
    start_end_date = session.query(Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).group_by(Measurement.date).all()
    start_end_list = list(start_end_date)
    return jsonify (start_end_list)

if __name__=='__main__':
  app.run(debug=True)
   
    
    

    
























