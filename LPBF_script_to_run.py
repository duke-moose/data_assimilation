##!/usr/bin/python
##LPBF Data Collection Program for NOAA and USGS Salinity and Wind Stations
##Program language: Python 3
##Program version: 1.1 / 1-20-2013 [P.Connor]
##Program update: 2.0 / 11-30-2018 [M. Salmon]

from datetime import datetime
import Assimilation_Tool as at
import platform

# 1. Make sure the following path is located on your system. Change Drive letter to match your system.
# 2. File "NOAApsuList.txt" must be present in the "Salinity_NOAA" directory.
# 3. File "USGSpsuList.txt" must be present in the "Salinity_USGS" directory.
# 4. File "NOAAwindList.txt" must be present in the "Wind_NOAA" directory.
# 5. Future stations can be added to their respective files without re-coding... just append new station number.

if platform.system() in "Windows":
    file_path = 'G:\\users\\COASTAL\\Hydrocoast\\Data Assimilation\\Data\\data_assimilation'
elif platform.system() in "Linux":
    file_path = '/home/sogood/Documents/Python/LPBF/Data Assimilation/Data/data_assimilation'

# NOAA Salinity Stations
NOAA_sal_dir = 'Salinity_NOAA'
NOAA_sal_url = 'https://www.ndbc.noaa.gov/data/realtime2/'
NOAA_sal_sta_file = 'NOAApsuList.txt'

# USGS Salinity Stations
USGS_sal_dir = 'Salinity_USGS'
USGS_sal_url = 'https://waterdata.usgs.gov/nwis/uv?&cb_00480=on&format=rdb&period=10&site_no='
USGS_sal_sta_file = 'USGSpsuList.txt'

# NOAA Wind Stations
NOAA_wind_dir = 'Wind_NOAA'
NOAA_wind_url = 'https://www.ndbc.noaa.gov/data/realtime2/'
NOAA_wind_sta_file = 'NOAAwindList.txt'

# Get date for today.
# Identifies previous Monday and uses this to begin all file and calculation imports.
today = datetime.today()
file_date = at.tool_filters.make_monday(today)

start_date = at.tool_filters.date_adjustment(file_date)
end_date = at.tool_filters.date_adjustment(start_date, day = -7)

# NOAA Ocean Data Setup and Processing
at.data_collection.scrape_gauges(NOAA_sal_dir, file_path, NOAA_sal_url, NOAA_sal_sta_file, file_date)
at.data_collection.save_gauge_to_csv(NOAA_sal_dir, file_path, start_date, end_date)
at.calculations.average_all_values(NOAA_sal_dir, file_path, start_date, end_date)

# USGS Salinity Data Setup and Processing
at.data_collection.scrape_gauges(USGS_sal_dir, file_path, USGS_sal_url, USGS_sal_sta_file, file_date)
at.data_collection.save_gauge_to_csv(USGS_sal_dir, file_path, start_date, end_date)
at.calculations.average_all_values(USGS_sal_dir, file_path, start_date, end_date)

# NOAA NDBC Buoys to collect wind data
at.data_collection.scrape_gauges(NOAA_wind_dir, file_path, NOAA_wind_url, NOAA_wind_sta_file, file_date)
at.data_collection.save_gauge_to_csv(NOAA_wind_dir, file_path, start_date, end_date)
at.calculations.average_hourly_values(NOAA_wind_dir, file_path, start_date, end_date)
