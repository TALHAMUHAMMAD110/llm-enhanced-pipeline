from client import minio_client
import os
from helper import calculate_seconds_since_last_modified

BATCH_TIME_SECONDS = 10  


def extracting_files_from_bucket():
    input_bucket = os.getenv("INPUT_BUCKET", "output-bucket")
    files_names = []
    try:
        response = minio_client().list_objects_v2(Bucket=input_bucket)
        print(f"Files in '{input_bucket}' bucket:")
        for obj in response.get("Contents", []):
            if (
                obj["Key"].endswith(".json")
                and calculate_seconds_since_last_modified(
                    obj["LastModified"].isoformat()
                )
                <= BATCH_TIME_SECONDS
            ):
                files_names.append(obj["Key"])

        print(f" {len(files_names)} new docs extracted for processing")

    except Exception as e:
        print(f"Error listing objects from MinIO: {e}")

    return files_names
