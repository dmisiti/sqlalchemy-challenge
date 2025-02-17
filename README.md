# SQLAlchemy Analysis of Hawaii Weather Observations

In this analysis, Python and SQLAlchemy were used to do an analysis and data exploration of a particular SQLite climate database including two tables describing weather observations in Hawaii.

### Analysis

First, SQLAlchemy was used to connect Python to a SQLite database with the weather data.

Then, two sets of analysis were performed:
- Precipitation Analysis: A graph was generated showing the precipitation levels in Hawaii over the most recent 12 months of data.
- Station Analysis: A histogram was generated showing the frequency of temperature observations over the most recent 12 months of data at the most active station.

### Flask API

Finally, a climate app was developed using Python on Flask, based on the SQLAlchemy queries from the analysis. Routes displayed on the app include data display for:
- Precipitation Data
- Station Data
- Temperature Data (Most Active Station)
- Temperature Data (Given Start Date)
- Temperature Data (Given Start and End Dates)

### Repository Structure

The `SurfsUp` folder contains:
- A `climate.ipynb` file with the Precipitation Analysis and Station Analysis
- An `app.py` file with the Flask API script

The `Resources` folder contains:
- The `hawaii.sqlite` database file with all climate data
- Two CSV files for easier view of each table in the database (`hawaii_measurements.csv` and `hawaii_stations.csv`)
