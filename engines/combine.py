import json
import subprocess
import os
from engines.gps import find_nearest_gps
from datetime import datetime, timedelta


def combine_gps_frame(frames_data, gps_data):
    gps_created = gps_data[0].get("time")
    video_created = frames_data.get("video_created_at")

    initial_offset = (
        gps_created - video_created
    ).total_seconds()

    final_metadata = {
        "job_id": frames_data.get("job_id"),
        "video_created": video_created,
        "gps_created": gps_created,
        "data": frames_data['frames']
    }
    print("Creation time gps: ", gps_created)
    print("Creation time video: ", video_created)
    print("Initial offset:", initial_offset)

    for idx, data in enumerate(final_metadata['data']):
        time_in_video = data.get("time_in_video")
        gps_time = video_created + timedelta(
            seconds=time_in_video+initial_offset
        )

        gps_point = find_nearest_gps(gps_data, target_time=gps_time)
        if gps_point is None:
            continue

        data.update(
            {
                "gps_time": gps_time.isoformat(),
                "lat": gps_point["lat"],
                "lon": gps_point["lon"]
            }
        )

    return final_metadata

    # while True:
    #     ret, frame = cap.read()
    #     if not ret:
    #         break

    #     if idx_frame % frame_interval == 0:
    #         time_in_video = idx_frame / fps
    #         gps_time = VIDEO_START_TIME + \
    #             timedelta(seconds=time_in_video+initial_offset)

    #         gps_point = find_nearest_gps(gps_points, gps_time)
    #         if gps_point is None:
    #             idx_frame += 1
    #             continue
    #         saved += 1
    #         os.makedirs(images_path, exist_ok=True)
    #         img_name = f"frame_{idx_frame:05d}.jpg"
    #         img_abs_path = os.path.join(images_path, img_name)
    #         img_rel_path = os.path.join("images", img_name)
    #         cv2.imwrite(img_abs_path, frame)

    #         metadata.append({
    #             "frame": idx_frame,
    #             "video_time": round(time_in_video, 2),
    #             "image_file": img_rel_path,
    #             "gps_time": gps_time.isoformat(),
    #             "lat": gps_point["lat"],
    #             "lon": gps_point["lon"]
    #         })

    #     idx_frame += 1

    # cap.release()

    # with open("metadata.json", "w") as file:
    #     json.dump(metadata, file)

    # return metadata
