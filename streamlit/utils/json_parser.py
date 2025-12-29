import pandas as pd

def flatten_result(result: list) -> pd.DataFrame:
    rows = []
    for item in result:
        for det in item["detection"]:
            rows.append({
                "frame": item["frame"],
                "time_in_video": item["time_in_video"],
                "frame_file": item["frame_file"],
                "gps_time": item["gps_time"],
                "lat": item["lat"],
                "lon": item["lon"],
                "class_id": det["class_id"],
                "confidence": det["confidence"],
                "bbox": det["bbox"],
            })
    return pd.DataFrame(rows)
