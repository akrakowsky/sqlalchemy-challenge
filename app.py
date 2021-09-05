import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement
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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start/<start><br/>"
        f"/api/v1.0/start/<start>/end/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_prcp = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_prcp.append(precipitation_dict)

    return jsonify(all_prcp)

    
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all passengers
    results = session.query(Station.station).distinct().all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Find the last date and convert it to date format
    last_date = session.query(Measurement).order_by(Measurement.date.desc()).first()
    final_date = dt.datetime.strptime(last_date.date, '%Y-%m-%d').date()

    # Retrieve the last 12 months of temperature data
    query_year = final_date - dt.timedelta(days=364)

    # Find the most active station
    act_stn = [Measurement.station, func.count(Measurement.station)]
    active_station = session.query(*act_stn).group_by(Measurement.station).\
                    order_by(func.count(Measurement.station).desc()).first().station

    # Gather the last 12 months of temperature measurements of the most active station 
    active_temp = session.query(Measurement.date, Measurement.tobs).\
                        filter(func.strftime('%Y-%m-%d', Measurement.date) > query_date).\
                        filter(Measurement.station == active_station).all()
    
    # Close Session
    session.close()
    
    #Return a JSON list of temperature observations (TOBS) for the previous year
    top_temp = []
    for date, tobs in active_temp:
        active_dict = {}
        active_dict["date"] = date
        active_dict["tobs"] = temperature
        top_temp.append(active_temp)
        
    return jsonify(top_temp)


@app.route("/api/v1.0/start/<start>")
def start_date(start):
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the date greater than or equal to start
    sel = [func.min(measurement.tobs),
           func.avg(measurement.tobs),
           func.max(measurement.tobs)
    ]
    
    
    start_filter = session.query(*sel).filter(measurement.date >= start).all()
    start_list = [
        {"TMIN": start_filter[0][0]},
        {"TAVG": start_filter[0][1]},
        {"TMAX": start_filter[0][2]}
    ]
    if start <= '2017-08-23':
        return jsonify(start_list)
    else:
        return jsonify("Error: Data is not available for dates before 2017-08-23, please enter a prior date.'")

    session.close()

@app.route("/api/v1.0/start/<start>/end/<end>")
def start_end(start, end):
     # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the date greater than or equal to start
    sel = [func.min(measurement.tobs),
           func.avg(measurement.tobs),
           func.max(measurement.tobs)
    ]
    
    
    start_end_filter = session.query(*sel).\
        filter(measurement.date.between(start,end)).all()
    start_end_list = [
        {"TMIN": start_end_filter[0][0]},
        {"TAVG": start_end_filter[0][1]},
        {"TMAX": start_end_filter[0][2]}
    ]
    if (start <= '2017-08-23') and (end >='2010-01-01') :
        return jsonify(start_end_list)
    else:
        return jsonify("Error: Please enter a start and end date between 2010-01-01 and 2017-08-23.")
    

 

    session.close()
if __name__ == '__main__':
    app.run(debug=True)    
