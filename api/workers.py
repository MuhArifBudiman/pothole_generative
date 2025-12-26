from .logger import logger
from .job_manager import update_job, get_job_path

# modul
from engines.gps import extract_gps
from engines.frame import get_frame
from engines.combine import combine_gps_frame
from src.inference import predict

import os
import json
import traceback


def process_job(job_id):
    try:
        logger.info(f"[{job_id}] Start processing")

        job_path = get_job_path(job_id=job_id)
        raw_path = os.path.join(job_path, 'raw')

        video_file = "video.mp4"
        gps_file = "track.gpx"

        # 1. GPS processing
        gps_data = extract_gps(job_id=job_id,
                               gps_file=f"raw/{gps_file}")
        update_job(job_id=job_id, progress=25)
        logger.info(f"[{job_id}] GPS extracted")

        # 2. Frame
        frames_data = get_frame(
            job_id=job_id,
            video_file=f"raw/{video_file}"
        )
        update_job(job_id=job_id, progress=50)
        logger.info(f"[{job_id}] Frames extracted")

        # 3 Combine gps and frame
        metadata = combine_gps_frame(
            frames_data=frames_data,
            gps_data=gps_data
        )
        update_job(job_id=job_id, progress=70)
        logger.info(f"[{job_id}] Metadata created!")

        with open(os.path.join(job_path, "metadata.json"), "w") as file:
            json.dump(metadata, file, indent=2, default=str)

        # 4 Inference YOLO
        predict_result = predict(
            job_id=job_id,
            metadata=metadata,
            batch=15
        )
        predict_result["video_created"] = predict_result["video_created"].isoformat()

        predict_result["gps_created"] = predict_result["gps_created"].isoformat()

        update_job(job_id=job_id, progress=100, status="done")
        with open(os.path.join(job_path, "result.json"), "w") as file:
            json.dump(predict_result, file, indent=2)

    except Exception as e:
        logger.error(f"[{job_id}] FAILED")
        logger.error(traceback.format_exc())
        update_job(job_id=job_id, status='Failed')
