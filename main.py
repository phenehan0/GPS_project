import datetime
from gps_functions import read_csv_data, calculate_distance, calculate_time_deltas
from gps_functions import log_error_or_warning, calc_distance_on_earth, GCS_Coordinates


if __name__ == "__main__":
    csv_data = read_csv_data()
    time_deltas_unsorted = calculate_time_deltas(csv_data["timestamp"])
    walks = []
    walk_started_at = datetime.datetime.strptime(csv_data["timestamp"][0], "%Y-%m-%d %H:%M:%S +0000").timestamp()
    slice_start = 0
    deltas = []
    for idx, i in enumerate(time_deltas_unsorted):
        if idx > 0 and i - time_deltas_unsorted[idx - 1] >= 1000:
            walk_ended_at = datetime.datetime.strptime(csv_data["timestamp"][idx], "%Y-%m-%d %H:%M:%S +0000").timestamp()
            walk = {k: csv_data[k][slice_start:idx + 1] for k in csv_data}
            walk["time_elapsed"] = sum(deltas)
            
            deltas = []
            walks.append(walk)

            slice_start = idx + 1
            walk_started_at = walk_ended_at

        else:
            deltas.append(i)
    if len(deltas)>0:
        walk = {k: csv_data[k][slice_start:] for k in csv_data}
        walk["time_elapsed"] = sum(deltas)
        deltas = []
        walks.append(walk)
        
    idx = 0
    for w_idx, walk in enumerate(walks):
        print("\n")
        print("==================WALK "+str(w_idx+1)+"=========================")
        print("STARTED AT: "+walk["timestamp"][0])
        print("ENDED AT: "+walk["timestamp"][1])

        latitude = walk["latitude"]
        longitude = walk["longitude"]
        time_elapsed = walk["time_elapsed"]
        total_distance = 0
        for i in range(0, len(latitude)):
            if i > 0:
                coords1 = GCS_Coordinates(float(latitude[i - 1]), float(longitude[i - 1]))
                coords2 = GCS_Coordinates(float(latitude[i]), float(longitude[i]))
                point1 = coords1.coordinates
                point2 = coords2.coordinates
                distance_km = calc_distance_on_earth(point1, point2)
                meters = distance_km*1000
            
                seconds = (time_deltas_unsorted[idx-1])
                if seconds < 1:
                    print(log_error_or_warning("timestamp", idx, "A positive number of seconds has not elapsed between measurements (seconds elapsed="+str(seconds)+")", "warning"))
                else:  
                    total_distance += distance_km
                
            if float(walk["speed"][i]) < 0:
                print(log_error_or_warning("speed", idx, "Speed cannot be negative", "error"))

            idx += 1

        minutes_elapsed = time_elapsed/60
        speed = (total_distance * (60/minutes_elapsed))
        print("Speed (Km/h): "+str(speed))
        print("Distance (Km): "+str(total_distance))
        print("\n\n\n")