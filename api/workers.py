from api.logger import logger
from api.job_manager import update_job

# modul
from engines.gps import extract_gps
from engines.frame import combine_gps_frame
from src.inference import predict


def process_job(job_id, video_path, gpx_path):
    pass
