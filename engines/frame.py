import json
from datetime import datetime
import subprocess
import cv2
import os
from .gps import extract_gps, find_nearest_gps
from datetime import datetime, timedelta


def get_video_creation_time(video_path: str) -> datetime:
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-show_entries", "format_tags=creation_time",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_path
    ]

    output = subprocess.check_output(cmd).decode().strip()

    if not output:
        raise ValueError("creation_time not found")

    return datetime.fromisoformat(output.replace("Z", "+00:00"))


def combine_gps_frame(video_file, gps_file, images_path):

    if not os.path.exists(video_file):
        raise ValueError(f"File {video_file} not found")

    cap = cv2.VideoCapture(video_file)
    fps = cap.get(cv2.CAP_PROP_FPS)

    idx_frame = 0
    saved = 0
    frame_interval = int(fps * 1)

    gps_points = extract_gps(gps_file)
    VIDEO_START_TIME = get_video_creation_time(video_path=video_file)

    initial_offset = (
        gps_points[0]["time"] - VIDEO_START_TIME
    ).total_seconds()

    print("Creation time gps: ", gps_points[0])
    print("Creation time video: ", VIDEO_START_TIME)
    print("Initial offset:", initial_offset)

    metadata = []

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if idx_frame % frame_interval == 0:
            time_in_video = idx_frame / fps
            gps_time = VIDEO_START_TIME + \
                timedelta(seconds=time_in_video+initial_offset)

            gps_point = find_nearest_gps(gps_points, gps_time)
            if gps_point is None:
                idx_frame += 1
                continue
            saved += 1
            os.makedirs(images_path, exist_ok=True)
            img_name = f"frame_{idx_frame:05d}.jpg"
            img_abs_path = os.path.join(images_path, img_name)
            img_rel_path = os.path.join("images", img_name)
            cv2.imwrite(img_abs_path, frame)

            metadata.append({
                "frame": idx_frame,
                "video_time": round(time_in_video, 2),
                "image_file": img_rel_path,
                "gps_time": gps_time.isoformat(),
                "lat": gps_point["lat"],
                "lon": gps_point["lon"]
            })

        idx_frame += 1

    cap.release()

    with open("metadata.json", "w") as file:
        json.dump(metadata, file)

    return metadata


if __name__ == '__main__':
    metadata = combine_gps_frame(
        video_file="sample.mp4",
        gps_file="sample.gpx"
    )

    print(len(metadata))
    print(metadata[0])
