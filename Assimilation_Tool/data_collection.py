import os
import urllib.request
import urllib.error
import csv
import Assimilation_Tool.tool_filters

def scrape_gauges(file_dir, file_path, url, station_file, date):
# Accesses station URL location and collects data from specific file.
# Files are specified in a TXT file.

    # Locate TXT file that identifies desired stations.
    # Locate directory to save output data
    station_list = os.path.join(file_path, file_dir, station_file)
    outdir = os.path.join(file_path, file_dir, date, 'raw')

    print("\t\t(LPBF Data Collection Program for {} Stations)\n".format(file_dir))

    # Check to see if directory already exists, if it does not the directory is created.
    if not os.path.isdir(outdir):
        os.makedirs(outdir)

    print("Please wait while data is collected.\n")

    # Save raw gauge data to a TXT file in user specified location.
    with open(station_list, 'r') as infile:
        for line in infile:
            print(line)
            outfile = line.rstrip() + '_' + date + '.txt'

            # Check url to see if it exists. If it doesn't exist print an error message.
            try:
                urllib.request.urlretrieve(url + line, os.path.join(outdir, outfile))

            except urllib.error.HTTPError:
                print('No file created. Error locating station {}'.format(line))

    print('{} output save location = '.format(file_dir) + outdir + "\n\n")


def save_gauge_to_csv(file_dir, file_path, start_date, end_date):
# Filters raw data TXT files to desired data range and saves them as CSV for
# easier use by LPBF.

    print("\t\t({} Stations being filtered and saved to CSV)\n".format(file_dir))

    # Convert datetime.datetime object to string to find correct directory.
    date = str(start_date.year) + str(start_date.month) + str(start_date.day)

    # Locate directory of TXT files to read.
    # Locate directory to save CSV files.
    txtfile_dir = os.path.join(file_path, file_dir, date, 'raw')
    csvfile_dir = os.path.join(file_path, file_dir, date, 'date_filtered_csv')

# Check to see if directory already exists, if it does not the directory is created.
    if not os.path.isdir(csvfile_dir):
        os.makedirs(csvfile_dir)

    # Loop through text files, filter, and save desired output in CSV.
    for station in os.listdir(txtfile_dir):
        txtfile_path = os.path.join(txtfile_dir, station)

        # Check that item is a file. Only TXT files should be saved here.
        if os.path.isfile(txtfile_path):
            txtfile = txtfile_path
            csvfile = os.path.join(csvfile_dir, str(station.rsplit(".",1)[0])+".csv")

            txt_lines = []

            with open(txtfile, 'r') as infile, open(csvfile, 'w') as outfile:
                for line in infile:
                    inner_list = [line.strip() for line in line.split()]
                    txt_lines.append(inner_list)

                # Initiate filter based on Station Type.
                if file_dir is 'Salinity_NOAA':
                    csv_lines = Assimilation_Tool.tool_filters.NOAA_ocean_filter(txt_lines, start_date, end_date)
                elif file_dir is 'Salinity_USGS':
                    csv_lines = Assimilation_Tool.tool_filters.USGS_salinity_filter(txt_lines, start_date, end_date)
                elif file_dir is 'Wind_NOAA':
                    csv_lines = Assimilation_Tool.tool_filters.NOAA_wind_filter(txt_lines, start_date, end_date)

                writer = csv.writer(outfile)
                writer.writerows(csv_lines)