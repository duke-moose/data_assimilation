from datetime import datetime

def try_strptime(s):
# Converts various user inputted date formats to datetime.datetime object.
# Input is a string date.
# Output is a date time object of input.

    fmts=["%m/%d/%Y %H:%M",
          "%m/%d/%y %H:%M",
          "%m-%d-%Y %H:%M",
          "%m-%d-%y %H:%M",
          "%m/%d/%Y",
          "%m/%d/%y",
          "%m-%d-%Y",
          "%m-%d-%y",
          "%Y%m%d",
          "%Y-%m-%d %H:%M"]
    for fmt in fmts:
        try:
            return datetime.strptime(s, fmt)
        except:
            continue

    print("Date format must be M/D/YYYY H:M, M/D/YY H:M, M-D-YYYY H:M, M-D-YY H:M, ")
    print("m/d/Y, m/d/y, m-d-Y, m-d-y, Ymd, or Y-m-d H:M")


def date_adjustment(start_date, month=0, day=0, year=0):
# Adjusts date by a user defined number of months, days, or years.
# Input is date string or datetime.datetime object.
# Output is adjusted datetime.datetime object based on user inputs.

    # Convert string date to datetime.datetime object.
    if type(start_date) is not type(datetime.today()):
        start_date = try_strptime(start_date)

    start_date = start_date.toordinal() + day
    start_date = datetime.fromordinal(start_date)

    month = start_date.month + month
    while month < 1:
        month = 12 + month
        year -= 1

    while month > 12:
        month = month - 12
        year += 1

    day = start_date.day
    year = start_date.year + year
    adj_date = start_date.replace(month=month, day=day, year=year)
    return adj_date

def make_monday(date):
# Converts any date to the previous Monday in string format YYMMDD.
    if type(date) is not type(datetime.today()):
        date = try_strptime(date)

    # datetime assumes Monday is 0 and Sunday is 6.
    shift = 0 - date.weekday()
    monday = date_adjustment(date, day=shift).strftime('%Y%m%d')
    return monday

def filter(LPBF_dict, txt_lines, start_date, end_date):
    # Filters input file to user defined date range.
    # Input path to station txt or csv file, start_date and end_date datetime.datetime objects..
    # Output CSV file of salinity values from start_date to end_date datetime.datetime objects.

    csv_lines = []
    # Search for the NOAA organization with year, month, day, hour, and minute in
    # multiple columns.

    if all (key in LPBF_dict["file_organization"] for key in ["year", "month", "day", "hour", "minute"]):
        year = LPBF_dict["file_organization"]["year"]
        month = LPBF_dict["file_organization"]["month"]
        day = LPBF_dict["file_organization"]["day"]
        hour = LPBF_dict["file_organization"]["hour"]
        minute = LPBF_dict["file_organization"]["minute"]
        header = LPBF_dict["first_col_header"]

        for line in txt_lines:
            try:
                # First two lines of these files contain the following headers.
                # Filter starts at lines with dates. This might change in the future.
                if line[year] in header:
                    csv_lines.append(line)
                elif int(line[month]) <= 12:
                    d_t = line[month] + "/" + line[day] + "/" + line[year] + " " + line[hour] + ":" + line[minute]
                    d_t = try_strptime(d_t)

                    if d_t <= start_date and d_t >= end_date:
                        csv_lines.append(line)
            except ValueError:
                pass
            except IndexError:
                pass

    elif all (key in LPBF_dict["file_organization"] for key in ["station_owner", "station_date", "station_time"]):
        station_owner = LPBF_dict["file_organization"]["station_owner"]
        station_date = LPBF_dict["file_organization"]["station_date"]
        station_time = LPBF_dict["file_organization"]["station_time"]
        header = LPBF_dict["first_col_header"]

        for line in txt_lines:
            try:
                # Begins filter past initial station text because the first line of data
                # contains "USGS" name. This might change in the future.
                if line[station_owner] in header:
                    d_t = (line[station_date] + " " + line[station_time])
                    d_t = try_strptime(d_t)
                    if d_t <= start_date and d_t >= end_date:
                        csv_lines.append(line)
            except IndexError:
                pass
    else:
        print("Need to make a new filter format for this station file.")
        # Below here is the place to add new filters as they become necessary.

    return (csv_lines)