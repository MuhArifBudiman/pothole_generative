from pydantic import BaseModel
from typing import Optional, List, Dict


class JobCreateResponse(BaseModel):
    job_id: str
    status: str


class JobStatusResponse(BaseModel):
    job_id: str
    progress: int
    status: str


class ResultResponse(BaseModel):
    job_id: str
    summary: Dict
    detections: List[Dict]
