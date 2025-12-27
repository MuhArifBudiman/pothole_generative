from engines.gps import find_nearest_gps
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


def combine_gps_frame(frames_data, gps_data):
    gps_created = gps_data[0].get("time")
    video_created = frames_data.get("video_created_at")
    if video_created is None:
        video_created = gps_created

    initial_offset = (
        gps_created - video_created
    ).total_seconds()

    final_metadata = {
        "job_id": frames_data.get("job_id"),
        "video_created": video_created,
        "gps_created": gps_created,
        "data": frames_data['frames']
    }
    logger.info("Creation time gps: {gps_created}")
    logger.info("Creation time video: {video_created}")
    logger.info("Offset video: {initial_offset}")
    # print("Creation time gps: ", gps_created)
    # print("Creation time video: ", video_created)
    # print("Initial offset:", initial_offset)

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
