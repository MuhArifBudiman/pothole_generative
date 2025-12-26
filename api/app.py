from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from fastapi import UploadFile, BackgroundTasks
from fastapi import HTTPException

import os
import shutil
from threading import Thread
import json

from .job_manager import create_job, get_job_path, get_job
from .workers import process_job

from fastapi import FastAPI, UploadFile, File


class JobCreateResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    progress: int
    status: str


class ResultResponse(BaseModel):
    job_id: str
    video_created: str
    gps_created: str
    data: List[Dict[str, Any]]


app = FastAPI(title="Pothole Detection")


@app.post("/request", response_model=JobCreateResponse)
def process(video: UploadFile = File(...),
            gps: UploadFile = File(...)):

    job_id = create_job()
    job_path = get_job_path(job_id)
    raw_path = os.path.join(job_path, "raw")

    # save files
    with open(os.path.join(raw_path, "video.mp4"), "wb") as f:
        shutil.copyfileobj(video.file, f)

    with open(os.path.join(raw_path, "track.gpx"), "wb") as f:
        shutil.copyfileobj(gps.file, f)

    # run worker async
    Thread(target=process_job, args=(job_id,)).start()

    return {
        "job_id": job_id,
        "status": "processing"
    }


@app.get("/job/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str):
    job = get_job(job_id)

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "status": job["status"],
        "progress": job.get("progress", 0)
    }


@app.get("/job/{job_id}/result", response_model=ResultResponse)
def get_result(job_id: str):
    job_path = get_job_path(job_id)
    result_path = os.path.join(job_path, "result.json")

    if not os.path.exists(result_path):
        raise HTTPException(
            status_code=404,
            detail="Result not available yet"
        )

    with open(result_path) as f:
        result = json.load(f)

    return result
