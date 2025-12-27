from datetime import datetime
import subprocess
import cv2
import os
from datetime import datetime
from api.logger import logger


# logger = logging.getLogger(__name__)

JOBS_DIR = "jobs"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_video_creation_time(video_file: str) -> datetime:
    cmd = [
        "ffprobe",
        "-v", "quiet",
        "-show_entries", "format_tags=creation_time",
        "-of", "default=noprint_wrappers=1:nokey=1",
        video_file
    ]

    output = subprocess.check_output(cmd).decode().strip()

    if not output:
        return None

    return datetime.fromisoformat(output.replace("Z", "+00:00"))


def get_frame(job_id: str, video_file: str):
    job_path = os.path.join(ROOT_DIR, JOBS_DIR, job_id)
    frames_path = os.path.join(job_path, "frames")
    video_path = os.path.join(job_path, video_file)

    if not os.path.exists(video_path):
        raise ValueError(f"File {video_path} not found")

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    logger.info(f"[{job_id}] Video FPS detected: {fps}")

    idx_frame = 0
    saved = 0
    frame_interval = int(fps * 1)

    try:
        video_start_time = get_video_creation_time(video_file=video_path)
    except Exception:
        video_start_time = None
        logger.warning(f"[{job_id}] Video has no creation time")

    metadata = {
        "job_id": job_id,
        "video_created_at": video_start_time,
        "fps": fps,
        "frames": []
    }

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        if idx_frame % frame_interval == 0:
            time_in_video = idx_frame/fps
            saved += 1

            os.makedirs(frames_path, exist_ok=True)
            frame_name = f"frame_{idx_frame:05d}.jpg"
            frame_abs_path = os.path.join(frames_path, frame_name)
            frame_real_path = os.path.join("frames", frame_name)
            cv2.imwrite(frame_abs_path, frame)

            metadata["frames"].append(
                {
                    "frame": idx_frame,
                    "time_in_video": time_in_video,
                    "frame_file": frame_real_path
                }
            )
        idx_frame += 1

    return metadata
