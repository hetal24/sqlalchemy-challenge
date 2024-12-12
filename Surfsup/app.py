# Import the dependencies.
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from flask import Flask, jsonify
from sqlalchemy.orm import Session


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine, reflect=True)
# print(Base.classes.keys())

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        
    )

def get_one_year_ago_date():
    """Calculate the date one year before the most recent date in the dataset."""
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    year, month, day = most_recent_date.split('-')
    one_year_ago = f"{int(year) - 1}-{month}-{day}"
    return one_year_ago

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipitation data for the last 12 months."""
    # Call the function to get the data
    one_year_ago = get_one_year_ago_date()
   
    # Query for date and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()

    session.close()
    #convert to dictionary
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    """Return a JSON list of stations."""
    results = session.query(Station.station).all()
    session.close()

    # Convert results to a list
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)


@app.route("/api/v1.0/tobs")
def tobs():
    """Retrieve dates and temperature observations of the most-active station for the last year."""
    # Find the most active station
    most_active_station = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count().desc()).first()[0]

    # Query the last year of temperature data for this station
    # Call the function to get the data
    one_year_ago = get_one_year_ago_date()
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date >= one_year_ago).all()
    session.close()

    # Convert results to a list of temperature observations
    tobs_list = [{"date": date, "temperature": temp} for date, temp in results]
    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature_stats(start, end=None):
    """Return TMIN, TAVG, TMAX for a given start or start-end range."""

    # Base query
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if end:
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    else:
        results = session.query(*sel).filter(Measurement.date >= start).all()

    session.close()

    # Convert results to a dictionary
    temp_stats = {
        "Start Date": start,
        "End Date": end if end else "N/A",
        "TMIN": results[0][0],
        "TAVG": results[0][1],
        "TMAX": results[0][2]
    }
    return jsonify(temp_stats)

if __name__ == "__main__":
    app.run(debug=True)