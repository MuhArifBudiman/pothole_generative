import requests

BASE_URL = "http://127.0.0.1:8000"

def create_job(video, gpx):
    return requests.post(
        f"{BASE_URL}/request",
        files={"video": video, "gps": gpx}
    )

def get_status(job_id):
    return requests.get(f"{BASE_URL}/job/{job_id}")

def get_result(job_id):
    return requests.get(f"{BASE_URL}/job/{job_id}/result")
