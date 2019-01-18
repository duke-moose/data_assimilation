import csv
import os
import math

def average(value_list):
    # Averages a list of float or integer values.

    if value_list:
        return sum(value_list)/len(value_list)
    else:
        return 'No Data'


def writedicttocsv(csv_file, csv_columns, dict_data):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in sorted(dict_data):
                writer.writerow(dict_data[data])
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
    return


def average_all_values(LPBF_dict, start_date, end_date=None):
    # Creates summary CSV with all stations averaged in a user defined date range.

    file_path = LPBF_dict["file_path"]
    file_dir = LPBF_dict["file_dir"]
    # Build date YYMMDD.
    # Create blank dictionary to save results.
    date = start_date.strftime('%Y%m%d')
    result = {}

    # Identify directory where CSV files are present.
    # Loop through CSV station files in directory and average them.
    csvfile_dir = os.path.join(file_path, date, 'date_filtered_csv')
    for station in os.listdir(csvfile_dir):
        csvfile = os.path.join(csvfile_dir, station)

        # Only run analysis on files.
        if os.path.isfile(csvfile):

            if file_dir is 'Salinity_NOAA':
                with open(csvfile, 'r') as infile:
                    sal = []
                    reader = csv.reader(infile)
                    for line in reader:
                        try:
                            # Only collect values that are not in the first
                            # few lines or 'MM', which is no data.
                            if line[8] not in ['SAL', 'psu', 'MM']:
                                sal.append(float(line[8]))
                        except IndexError:
                            pass
                        continue

            elif file_dir is 'Salinity_USGS':
                with open(csvfile, 'r') as infile:
                    sal = []
                    reader = csv.reader(infile)
                    for line in reader:
                        try:
                            # Convert to a float.
                            sal.append(float(line[5]))
                        except IndexError:
                            pass
                        continue

            elif file_dir is 'Wind_NOAA':
                with open(csvfile, 'r') as infile:
                    sal = []
                    reader = csv.reader(infile)
                    for line in reader:
                        try:
                            # Only collect values that are not in the first
                            # few lines or 'MM', which is no data.
                            if line[6] not in ['WSPD', 'm/s', 'MM']:
                                sal.append(float(line[6]))
                        except IndexError:
                            pass
                        continue

            # Fill dictionary with
                # key: station
                # value: average of all station values.
            result[station] = average(sal)

    # Create CSV file to save station averages.
    # Save results in CSV.
    result_file = os.path.join(file_path, date, "Averages.csv")
    with open(result_file, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in result.items():
            writer.writerow([key, value])


def average_hourly_values(LPBF_dict, start_date, end_date=None):
    # Creates summary CSV with wind speeds, directions, and East to West/North to South
    # vectors averaged for each station.

    file_path = LPBF_dict["file_path"]
    file_dir = LPBF_dict["file_dir"]
    # Build date YYMMDD.
    date = start_date.strftime('%Y%m%d')

    # Identify directory where CSV files are present.
    csvfile_dir = os.path.join(file_path, date, 'date_filtered_csv')

    # Loop through CSV station files in directory and average them.
    for station in os.listdir(csvfile_dir):
        csvfile = os.path.join(csvfile_dir, station)

        # Only run analysis on files.
        if os.path.isfile(csvfile):

            if file_dir is 'Wind_NOAA':
                with open(csvfile, 'r') as infile:
                    title = ['YYYYMMDD_HH', 'dir', 'speed', 'ew_vector', 'ns_vector']
                    result = {}
                    new_day = []
                    reader = csv.reader(infile)

                    for line in reader:
                        try:
                            # Only collect values that are not in the first
                            # few lines or 'MM', which is no data.
                            YYYY = line[0]
                            MM = line[1]
                            DD = line[2]
                            HR =line[3]
                            WDIR = line[5]
                            WSPD = line[6]
                            if DD not in ['DD', 'dy', 'MM']:
                                day = YYYY + MM + DD + '_' + HR

                                if WDIR not in ['MM'] and WSPD not in ['MM']:
                                    if day != new_day:
                                        wind_spd = []
                                        wind_dir = []
                                        ew_dir = []
                                        ns_dir = []
                                        wind_dir.append(float(WDIR))
                                        wind_spd.append(float(WSPD))
                                        ew_dir.append(math.sin(float(WDIR)*math.pi/180))
                                        ns_dir.append(math.cos(float(WDIR)*math.pi/180))
                                        new_day = YYYY + MM + DD + '_' + HR

                                    elif day == new_day:
                                        wind_dir.append(float(WDIR))
                                        wind_spd.append(float(WSPD))
                                        ew_dir.append(math.sin(float(WDIR) * math.pi / 180))
                                        ns_dir.append(math.cos(float(WDIR) * math.pi / 180))

                                    #Dictionary of results orgranized by date
                                    result[day] = {'YYYYMMDD_HH': day, 'dir': average(wind_dir),\
                                                     'speed': average(wind_spd), 'ew_vector': average(ew_dir),\
                                                     'ns_vector': average(ns_dir)}
                        except IndexError:
                            pass
                        continue

                    # Create CSV file to save station averages.
                    # Save results in CSV.
                    result_file = os.path.join(file_path, date, date + '_' + str(station.split('.')[0]) + "_NOAA_Wind.csv")
                    writedicttocsv(result_file, title, result)
