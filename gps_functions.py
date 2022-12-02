import csv, datetime, math


class GCS_Coordinates:
    def __init__(self, longitude, latitude):

        if longitude < -180 or longitude > 180:
            raise ValueError("longitude must be between -180 and 180 (inclusive)")
        
        if latitude < -90 or latitude > 90:
            raise ValueError("latitude must be between -90 and 90 (inclusive)")
                
        if type(longitude) != float or type(latitude) != float:
            raise ValueError("Longitude and latitude coordinates must both be floats")

        self.latitude = latitude
        self.longitude = longitude
        
    @property
    def coordinates(self):
        return (self.latitude, self.longitude)

def to_radians(theta):
    assert type(theta) == int or type(theta) == float
    pi = 3.1415926
    return pi * theta / 180
    
def haversine(point1, point2):
    dlat1, dlon1 = to_radians(point1[0]), to_radians(point1[1])
    dlat2, dlon2 = to_radians(point2[0]), to_radians(point2[1])
    delta_lat = dlat2 - dlat1
    delta_lon = dlon2 - dlon1
    return math.sin(delta_lat / 2)**2 + math.cos(dlat1) * math.cos(dlat2) * math.sin(delta_lon / 2)**2

def calc_distance_on_earth(point1, point2):
    h = haversine(point1, point2)
    radius_earth = 6371
    return radius_earth * (2 * math.asin(math.sqrt(h)))

def read_csv_data():
    csvData = []
    result = {}
    column_headers = []
    with open("gps_dataset.csv", "r") as f:
        csvData = csv.reader(f)
        csvData = list(csvData)
        columns = csvData[0][0]
        column_headers = columns.split(";")
        f.close()
    csvData = csvData[1:]
    for row_idx, row in enumerate(csvData):
        for col_idx, cell in enumerate(row[0].split(";")):
            try:
                result[column_headers[col_idx]].append(cell)
            except KeyError:
                result[column_headers[col_idx]] = [cell]
    return result

def calculate_time_difference(t1, t2):
    prev_tmp = datetime.datetime.strptime(t1, "%Y-%m-%d %H:%M:%S +0000").timestamp()
    tmp = datetime.datetime.strptime(t2, "%Y-%m-%d %H:%M:%S +0000").timestamp()
    return tmp - prev_tmp

def calculate_time_deltas(timestamps):
    time_deltas = []
    prev_tmp = timestamps[0]
    for t in timestamps[1:]:
        time_deltas.append(calculate_time_difference(prev_tmp, t))
        prev_tmp = t
    return time_deltas

def calculate_distance(latitude, longitude):
    total_distance_km = 0
    for i in range(1, len(latitude)):
        point1 = (float(latitude[i - 1]), float(longitude[i - 1]))
        point2 = (float(latitude[i]), float(longitude[i]))
        distance_km = calc_distance_on_earth(point1, point2)
        total_distance_km += distance_km
    return total_distance_km

def log_error_or_warning(column_name, row, msg, msg_type):
    message = ""
    if msg_type.lower() == "error":
        message += "[ERROR] "
    elif msg_type == "warning":
        message += "[WARNING] "
    message += "(column: '" + str(column_name) + "', row: "+str(row)+") "+str(msg)
    return message




        

        


