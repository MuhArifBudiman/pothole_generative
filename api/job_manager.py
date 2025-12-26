import uuid
import os
import json
from logger import logger


JOBS_DIR = "jobs"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_job():
    id = uuid.uuid4().hex[:8]
    job_path = os.path.join(ROOT_DIR, JOBS_DIR, id)

    os.makedirs(os.path.join(job_path, 'raw'), exist_ok=True)
    os.makedirs(os.path.join(job_path, 'frames'), exist_ok=True)

    metadata = {
        "id": id,
        "status": "queued",
        "progress": 0
    }

    with open(f"{job_path}/metadata.json", "w") as file:
        json.dump(metadata, file)
    logger.info(f"[{id}] Job created")

    return id


def update_job(job_id, **kwargs):
    path = f"{JOBS_DIR}/{job_id}/metadata.json"

    with open(path) as f:
        data = json.load(f)

    data.update(kwargs)

    with open(path, "w") as f:
        json.dump(data, f)

    logger.info(f"[{job_id}] Update job: {kwargs}")
