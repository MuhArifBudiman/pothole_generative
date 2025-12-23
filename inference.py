import os
import cv2
from ultralytics import YOLO
import json
from typing import List, Dict

DIR_FILE = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(DIR_FILE, "models", "yolo11n-seg.pt")

if not os.path.exists(MODEL_PATH):
    raise ValueError(f"No file directory {MODEL_PATH}")
else:
    yolo = YOLO(MODEL_PATH)

file = 'metadata.json'

with open(file, "r") as file:
    if file:
        metadata = json.load(file)
    else:
        raise ValueError("No metadata")


def predict(metadata: List, batch=10) -> List[Dict]:
    batch_images = []
    batch_meta = []

    all_result = []
    for item in metadata:
        img = cv2.imread(item.get("image_file"))

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
                    "detection": det
                }
            )

    return all_result


def save_json(result_file):
    with open("all_result_metadata.json", "w") as file:
        json.dump(result_file, file)


if __name__ == "__main__":
    result = predict(metadata=metadata)
    save_json(result_file=result)
