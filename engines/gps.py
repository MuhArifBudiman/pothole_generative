import json
import gpxpy
from typing import List, Dict
from datetime import datetime


def extract_gps(gps_file: str) -> List[Dict]:
    if not gps_file.endswith(".gpx"):
        raise ValueError("Please input gpx format file")

    with open(gps_file, "r") as file:
        print("Open gps file")
        gpx = gpxpy.parse(file)
        print("gps file opened")

    # ------ EXTRACT GPS-------
    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    "lat": point.latitude,
                    "lon": point.longitude,
                    "time": point.time  # datetime (UTC)
                })

    # with open("metadata_gps.json", "w") as file:
    #     json.dump(points, file)

    return points


def find_nearest_gps(gps_points, target_time: datetime):
    """
    Cari GPS point dengan waktu terdekat ke target_time
    """
    nearest = None
    min_diff = None

    for p in gps_points:
        diff = abs((p["time"] - target_time).total_seconds())

        if min_diff is None or diff < min_diff:
            min_diff = diff
            nearest = p

    return nearest


gps_points = extract_gps("gps/sample.gpx")

print("TOTAL GPS POINTS:", len(gps_points))
print("FIRST:", gps_points[0])
print("LAST :", gps_points[-1])
