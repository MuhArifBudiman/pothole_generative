import gpxpy
from typing import List, Dict
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

JOBS_DIR = "jobs"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def extract_gps(job_id, gps_file: str) -> List[Dict]:
    job_path = os.path.join(ROOT_DIR, JOBS_DIR, job_id)

    if not gps_file.endswith(".gpx"):
        raise ValueError("Please input gpx format file")

    with open(os.path.join(job_path, gps_file), "r") as file:
        gpx = gpxpy.parse(file)
        logger.info(f"GPS [{job_id}] opened")

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
