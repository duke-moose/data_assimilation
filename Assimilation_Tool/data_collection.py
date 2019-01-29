import os
import urllib.request
import urllib.error
import csv
import Assimilation_Tool.tool_filters

def scrape_gauges(LPBF_dict, date):
# Accesses station URL location and collects data from specific file.
# Files are specified in a TXT file.
    # Locate TXT file that identifies desired stations.
    # Locate directory to save output data
    file_path = LPBF_dict["file_path"]
    station_list = os.path.join(file_path, LPBF_dict["station_list"])
    url = LPBF_dict["url"]
    outdir = os.path.join(file_path, date, 'raw')

    print("\t\t(Data Collection Program for directory {})\n".format(file_path))

    # Check to see if directory already exists, if it does not the directory is created.
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    # Save raw gauge data to a TXT file in user specified location.
    with open(station_list, 'r') as infile:
        for station in infile:
            print(station)
            outfile = station.rstrip() + '_' + date + '.txt'

            # Check url to see if it exists. If it doesn't exist print an error message.
            try:
                urllib.request.urlretrieve(url + station, os.path.join(outdir, outfile))

            except urllib.error.HTTPError:
                print('No file created. Error locating station {}'.format(station))

    print('Save location = ' + outdir + "\n\n")


def save_gauge_to_csv(LPBF_dict, start_date, end_date):
# Filters raw data TXT files to desired data range and saves them as CSV for
# easier use by LPBF.
    file_path = LPBF_dict["file_path"]

    # Convert datetime.datetime object to string to find correct directory.
    date = start_date.strftime('%Y%m%d')

    # Locate directory of TXT files to read.
    # Locate directory to save CSV files.
    txtfile_dir = os.path.join(file_path, date, 'raw')
    csvfile_dir = os.path.join(file_path, date, 'date_filtered_csv')

# Check to see if directory already exists, if it does not the directory is created.
    if not os.path.isdir(csvfile_dir):
        os.makedirs(csvfile_dir)

    # Loop through text files, filter, and save desired output in CSV.
    for station in os.listdir(txtfile_dir):
        txtfile_path = os.path.join(txtfile_dir, station)

        print("Station {} being filtered and saved to CSV\n".format(station))

        # Check that item is a file. Only TXT files should be saved here.
        if os.path.isfile(txtfile_path):
            txtfile = txtfile_path
            csvfile = os.path.join(csvfile_dir, str(station.rsplit(".",1)[0])+".csv")

            txt_lines = []

            with open(txtfile, 'r') as infile, open(csvfile, 'w') as outfile:
                for line in infile:
                    inner_list = [line.strip() for line in line.split()]
                    txt_lines.append(inner_list)

                # Filter Stations by date
                csv_lines = Assimilation_Tool.tool_filters.filter(LPBF_dict, txt_lines, start_date, end_date)
                # Initiate filter based on Station Type.
                # if file_dir is 'Salinity_NOAA':
                    # csv_lines = Assimilation_Tool.tool_filters.NOAA_ocean_filter(txt_lines, start_date, end_date)
                # elif file_dir is 'Salinity_USGS':
                #     csv_lines = Assimilation_Tool.tool_filters.USGS_salinity_filter(txt_lines, start_date, end_date)
                # elif file_dir is 'Wind_NOAA':
                #     csv_lines = Assimilation_Tool.tool_filters.NOAA_wind_filter(txt_lines, start_date, end_date)

                writer = csv.writer(outfile)
                writer.writerows(csv_lines)