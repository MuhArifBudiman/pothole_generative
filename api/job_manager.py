import uuid
import os
import json
from .logger import logger


JOBS_DIR = "jobs"
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_job_path(job_id):
    return os.path.join(ROOT_DIR, JOBS_DIR, job_id)


def get_job(job_id):
    path = os.path.join(ROOT_DIR, JOBS_DIR, job_id, "job.json")

    if not os.path.exists(path):
        return None

    with open(path) as f:
        return json.load(f)


def create_job():
    job_id = uuid.uuid4().hex[:8]
    job_path = os.path.join(ROOT_DIR, JOBS_DIR, job_id)

    os.makedirs(os.path.join(job_path, 'raw'), exist_ok=True)
    os.makedirs(os.path.join(job_path, 'frames'), exist_ok=True)

    metadata = {
        "id": job_id,
        "status": "processing",
        "progress": 0,
        "stage":"starting to extract"
    }

    with open(f"{job_path}/job.json", "w") as file:
        json.dump(metadata, file)
    logger.info(f"[{job_id}] Job created")

    return job_id


def update_job(job_id, **kwargs):
    path = os.path.join(ROOT_DIR, JOBS_DIR, job_id, "job.json")

    with open(path) as f:
        data = json.load(f)

    data.update(kwargs)

    with open(path, "w") as f:
        json.dump(data, f)

    logger.info(f"[{job_id}] Update job: {kwargs}")
