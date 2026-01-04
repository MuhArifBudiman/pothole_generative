import pandas as pd


def flatten_result(result: list) -> pd.DataFrame:
    rows = []
    for item in result:
        for det in item["detection"]:
            rows.append({
                "frame": item["frame"],
                "time_in_video": item["time_in_video"],
                "frame_file": item["frame_file"],
                "frame_result_file": item["frame_result_file"],
                "gps_time": item["gps_time"],
                "latitude": item["latitude"],
                "longitude": item["longitude"],
                "class_id": det["class_id"],
                "confidence": det["confidence"],
                "bbox": det["bbox"],
                "total_detect": item['total_detect']
            })
    return pd.DataFrame(rows)
