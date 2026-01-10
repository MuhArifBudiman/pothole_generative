import os
from ultralytics import YOLO
from huggingface_hub import hf_hub_download
from loguru import logger

# cache dir aman untuk Railway & Windows
MODEL_DIR = os.getenv("MODEL_DIR", "/tmp/models")
os.makedirs(MODEL_DIR, exist_ok=True)

REPO_ID = "muh-arif21/final_project"
FILENAME = "best.pt"


def load_model():
    logger.info("Downloading model from HuggingFace if not exists...")

    model_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=FILENAME,
        cache_dir=MODEL_DIR,
        force_download=False
    )

    logger.info(f"Model loaded from: {model_path}")
    return YOLO(model_path)
