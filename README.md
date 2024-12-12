# sqlalchemy-challenge

## Climate Data Analysis

1. Use SQLAlchemy to:

    * Connect to the SQLite database hawaii.sqlite using create_engine.

    * Reflect the database tables with automap_base and map them to the Measurement and Station classes.

    * Create an SQLAlchemy ORM session.

2. Perform the following analyses:

    * Precipitation Analysis:
        
        Find the most recent date in the dataset.
        
        Query the last 12 months of precipitation data, selecting only the date and prcp values.
        
        Load the query results into a Pandas DataFrame, sort by date, and plot the data.
        
        Print the summary statistics of the precipitation data.
    * Station Analysis:
    
        Query the total number of stations in the dataset.
        
        Find the most active station (the station with the most observations).
        
        Query the minimum, maximum, and average temperatures for the most active station.
        
        Retrieve and plot the last 12 months of temperature observations for this station as a histogram with 12 bins.
        
        Close your SQLAlchemy session.


## Flask API

1. Create a Flask app and set up the following API routes:

    * /: List all available routes.
    
    * /api/v1.0/precipitation: Return the last 12 months of precipitation data as a JSON dictionary (date as key, precipitation as value).
    
    * /api/v1.0/stations: Return a JSON list of all weather stations.
    
    * /api/v1.0/tobs: Return a JSON list of temperature observations for the most active station from the last 12 months.
    
    * /api/v1.0/<start> and /api/v1.0/<start>/<end>:
        
        Return the minimum, average, and maximum temperatures for all dates greater than or equal to the start date.
        
        For a date range, calculate the same metrics for the inclusive range.

2. Use Flask's jsonify to format the query results as valid JSON responses.
