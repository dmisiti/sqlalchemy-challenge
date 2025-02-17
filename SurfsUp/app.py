# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

#################################################
# Database Setup
#################################################

# Connect to the database
engine = create_engine('sqlite:///../Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
Session = sessionmaker(bind=engine)
session = Session()

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Homepage
@app.route('/')
def home():
    return """
    <h1>Welcome to the Hawaii Weather API!</h1>
    <p>Here are the available routes:</p>
    <ul>
        <li>/api/v1.0/precipitation</li>
        <li>/api/v1.0/stations</li>
        <li>/api/v1.0/tobs</li>
        <li>/api/v1.0/YYYY-MM-DD   (insert start date)</li>
        <li>/api/v1.0/YYYY-MM-DD/YYYY-MM-DD    (insert start date/end date)</li>
    </ul>
    """

# Precipitation
@app.route('/api/v1.0/precipitation', methods=['GET'])
def precipitation():
    most_recent_date = session.query(func.max(Measurement.date)).scalar()
    one_year_ago = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).\
        all()
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation_dict)

# Stations
@app.route('/api/v1.0/stations', methods=['GET'])
def stations():
    stations = session.query(Station.station).all()
    station_list = [station[0] for station in stations]
    return jsonify(station_list)

# TOBS
@app.route('/api/v1.0/tobs', methods=['GET'])
def tobs():
    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]
    most_recent_date = session.query(func.max(Measurement.date)).\
        filter(Measurement.station == most_active_station).scalar()
    one_year_ago = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)
    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= one_year_ago).\
        all()
    tobs_list = [{"date": date, "temperature": tobs} for date, tobs in temperature_data]
    return jsonify(tobs_list)

# Start Date
@app.route('/api/v1.0/<start>', methods=['GET'])
def start_date(start):

    temperature_stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()

    return jsonify({
        "1_start_date": start,
        "2_min_temp": temperature_stats[0][0],
        "3_avg_temp": temperature_stats[0][1],
        "4_max_temp": temperature_stats[0][2]
    })

# Start-End Date
@app.route('/api/v1.0/<start>/<end>', methods=['GET'])
def start_end_dates(start, end):

    temperature_stats = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    return jsonify({
        "1_start_date": start,
        "2_end_date": end,
        "3_min_temp": temperature_stats[0][0],
        "4_avg_temp": temperature_stats[0][1],
        "5_max_temp": temperature_stats[0][2]
    })

if __name__ == '__main__':
    app.run(debug=True)