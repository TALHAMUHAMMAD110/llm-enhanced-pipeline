from datetime import datetime, timezone
from client import minio_client
import json
import re
import time
from datetime import datetime, timezone


def reading_files_from_bucket(bucket, source_file):
    try:
        response = minio_client().get_object(Bucket=bucket, Key=source_file)
        data = json.loads(response["Body"].read().decode("utf-8"))
        print(f"Successfully read '{source_file}' from '{bucket}' bucket")
        return data
    except Exception as e:
        print(f"Error reading {source_file}' from '{bucket}' bucket: {e}")


def calculate_seconds_since_last_modified(last_modified_str):

    try:
        last_modified = datetime.fromisoformat(last_modified_str)
        now = datetime.now(timezone.utc)
        diff = now - last_modified

        seconds = diff.total_seconds()
    except Exception as e:
        print(f"Error calculating seconds since last modified: {e}")
        seconds = None

    return seconds


def fetching_numbers_from_text(text):
    match = re.search(r"(\d+)", text)
    if match:
        return match.group(1)
    else:
        return None


def current_timestamp():
    try:
        return datetime.fromtimestamp(time.time(), timezone.utc)
    except Exception as e:
        print(f"Error converting timestamp: {e}")
        return None
