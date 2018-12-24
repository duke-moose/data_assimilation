# HYDROCOAST Map Data Collection
Prepared for: Lake Pontchartrain Basin Foundation
Prepared by: Matt Salmon

Link: [HYDROCOAST Maps](https://saveourlake.org/lpbf-programs/coastal/hydrocoast-maps/)

**Requirements**
1. Python3
2. Place data_assimlation in directory: G:\\users\\COASTAL\\Hydrocoast\\Data Assimilation\\Data\\data_assimilation


**Purpose:** 
This package collects salinity or wind speeds from select NOAA and USGS gauges.
Averages results to simplify map input.


**How to Modify Desired Gauge Stations**
NOAA and USGS stations are contained in a TXT files located in their respective directories.
To add or remove stations these files can be modified. Results are saved in their respective
directory. 


**Results**
By default, data is collected for the full week (i.e., seven days from a Sunday to the following Saturday).
Salinity values are averaged for the entire time frame. Wind speeds 
are averaged by hour for the entire time frame. All output files are saved as CSV in a
folder labeled by date.