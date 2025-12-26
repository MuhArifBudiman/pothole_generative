import os
import cv2
from ultralytics import YOLO
import json
from typing import List, Dict

DIR_FILE = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(DIR_FILE)
MODEL_PATH = os.path.join(ROOT_DIR, "models", "yolo11n-seg.pt")
JOBS_DIR = "jobs"


def load_model():
    if not os.path.exists(MODEL_PATH):
        raise ValueError(f"No file directory {MODEL_PATH}")
    return YOLO(MODEL_PATH)


def predict(job_id, metadata: Dict, batch=10) -> Dict[Dict, List]:
    yolo = load_model()

    job_path = os.path.join(ROOT_DIR, JOBS_DIR, job_id)
    batch_images = []
    batch_meta = []

    all_result = []
    if not isinstance(metadata.get("data"), list):
        raise ValueError("There's no frame + gps in metadata")
    else:
        for item in metadata.get("data"):
            img = cv2.imread(os.path.join(job_path, item.get("frame_file")))

            batch_images.append(img)
            batch_meta.append(item)

            if len(batch_images) == batch:
                detection = yolo(batch_images)

                for det, meta in zip(detection, batch_meta):
                    detections_json = []
                    boxes = det.boxes
                    if boxes is not None:
                        for box in boxes:
                            detections_json.append({
                                "class_id": int(box.cls[0]),
                                "confidence": float(box.conf[0]),
                                "bbox": box.xyxy[0].tolist()
                            })
                    all_result.append(
                        {
                            **meta,
                            "detection": detections_json,
                            "total_detect": len(detections_json)
                        }
                    )

                batch_images.clear()
                batch_meta.clear()

        if batch_images:
            detection = yolo(batch_images)

            for det, meta in zip(detection, batch_meta):
                detections_json = []
                boxes = det.boxes
                if boxes is not None:
                    for box in boxes:
                        detections_json.append({
                            "class_id": int(box.cls[0]),
                            "confidence": float(box.conf[0]),
                            "bbox": box.xyxy[0].tolist()
                        })
                all_result.append(
                    {
                        **meta,
                        "detection": detections_json,
                        "total_detect": len(detections_json)
                    }
                )
    metadata['data'] = all_result
    return metadata


def save_json(result_file):
    with open("all_result_metadata.json", "w") as file:
        json.dump(result_file, file)


if __name__ == "__main__":
    metadata_path = os.path.join(ROOT_DIR, "metadata.json")
    with open(metadata_path) as file:
        metadata = json.load(file)
    result = predict(metadata=metadata)
    print("Success predict")
    save_json(result_file=result)
    print("Saved to json")
