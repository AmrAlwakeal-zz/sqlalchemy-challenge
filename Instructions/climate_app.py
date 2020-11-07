import numpy as np
import csv
import json
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:/// hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

####################
# precipitation
####################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Convert the query results to a dictionary using date as the key and prcp as the value"""
    # Create our session (link) from Python to the DB
    session = Session(engine)

    
    # Query all Measurement
    results = session.query(Measurement).all()
    # Close the Query
    session.close()
    #Create a dictionary using 'date' as the key and 'prcp' as the value.
    year_prcp = []
    for result in results:
        result_dict = {}
        result_dict['date'] = result.date
        result_dict['prcp'] = result.prcp
        year_prcp.append(result_dict)
        # Jsonify summary
        return jsonify(year_prcp)
    
#######################
# stations
#######################
## Return a JSON list of stations from the dataset

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations data """
    
    result_2 = session.query(Station.station).all()
    station_list = []
    for station in result_2:
        station_dict = {}
        station_dict['station'] = results.station
        station_dict['name'] = results.name
        station_dict['latitude'] = result_2.latitude
        station_dict['longitude'] = result_2.longitude
        station_dict['elevation'] = result_2.elevation
        station_list.append(station_dict)
    return jsonify(station_list)    

####################
## tobs
###################
#### Query the dates and temperature observations of the most active station for the last year of data
####################

@app.route("/api/v1.0/tobs")
def tobs():

    active_station = session.query(Measurement.station, func.count(Measurement.tobs)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.tobs).desc()).all()
    temp_station = []
    for act in active_station:
        temp_dict ={}
        temp_dict['date'] = active_station.date
        temp_dict['station'] = active_station.station
        temp_dict['tobs'] = active_station.tobs
        temp_station.append(temp_dict)
    return jsonify(temp_station)

#########################
## start & end
##########################

@app.route("/api/v1.0/<start>/<end>")
def  (start, end):
    
    start_date = dt.datetime.strptime(start,'%Y-%m-%d')
    end_date = dt.datetime.strptime(end,'%Y-%m-%d')
    trip_days = dt.datetime.strptime
    trip_result = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    trip_temp = []
    for in trip_result:
        trip_dict = {}
        trip_dict[tmin] = trip_temp[0][0]
        trip_dict[tavg] = trip_temp[0][1]
        trip_dict[tmax] = trip_temp[0][2]
        trip_temp.append(trip_dict)
    return jsonify(trip_temp)




####################
####################

if __name__ == "__main__":
    app.run(debug=True)