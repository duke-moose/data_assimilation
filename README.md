# HYDROCOAST Map Data Collection
Prepared for: Lake Pontchartrain Basin Foundation  
Prepared by: Matt Salmon

Link: [HYDROCOAST Maps](https://saveourlake.org/lpbf-programs/coastal/hydrocoast-maps/)

**Requirements**
1. Python3
2. Place all files in directory: G:\\users\\COASTAL\\Hydrocoast\\Data Assimilation\\Data\\data_assimilation


**Purpose:**  
This package collects salinity or wind speeds from select NOAA and USGS gauges.
These values are filtered by date (i.e., Monday to Sunday), and averaged for the entire week (salinity) or hourly (wind speeds).
Results of this tool are used as inputs to HYDROCOAST Maps.


**How to Modify Desired Gauge Stations**  
All NOAA and USGS stations, where information is collected, are listed in  TXT files located in their respective directories.
Stations can be added or removed by:  

* Added: Opening the TXT file, adding a station on a new line at the bottom.
* Stations can be removed by deleting them.   

Results from the analysis are saved in a dated directory based on their source (i.e., NOAA Wind, NOAA Salinity, and USGS Salinity).
The date on the directory is based on the beginning of the week analyzed.

Result files include both 'raw' TXT files with all gauge data, and filtered CSV files containing only the current weeks worth of data.

**Results**  
By default, data is collected for the full week (i.e., seven days from Monday to the following Sunday).
Salinity results include a single weekly average for each station. Wind speed results include averages for each hour during a given week. All output files are saved as CSV in a
folder labeled by date.

**Data Sources**  
[NOAA](https://www.ndbc.noaa.gov/data/realtime2/)  
[USGS](https://waterdata.usgs.gov/nwis/uv?&cb_00480=on&format=rdb&period=10&site_no=)  
_Note: These links may change in the future_

**Directions**
file_path
url
add other descriptions