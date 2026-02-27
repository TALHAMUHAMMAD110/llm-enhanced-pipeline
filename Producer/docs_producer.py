import json
import time
import random
import os
from dotenv import load_dotenv
import boto3
from io import BytesIO

# Load environment variables from .env file
load_dotenv()

# Initialize MinIO client
minio_client = boto3.client(
    "s3",
    endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
    aws_access_key_id=os.getenv("MINIO_ROOT_USER", "minioadmin"),
    aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD", "minioadmin"),
    region_name="us-east-1",
)


def generating_json_docs():

    input_bucket = os.getenv("INPUT_BUCKET", "input-bucket")
    output_bucket = os.getenv("OUTPUT_BUCKET", "output-bucket")
    source_file = os.getenv("SOURCE_FILE_NAME", "test_documents_v2.json")

    offset = 3
    last_index = 0
    chunk_number = 1

    # Read source file from MinIO input bucket
    try:
        response = minio_client.get_object(Bucket=input_bucket, Key=source_file)
        data = json.loads(response["Body"].read().decode("utf-8"))
        print(f"Successfully read '{source_file}' from '{input_bucket}' bucket")
    except Exception as e:
        print(f"Error reading from MinIO: {e}")
        # Fallback to local file if MinIO fails
        with open(source_file, "r") as file:
            data = json.load(file)
        print(f"Fallback: read '{source_file}' from local storage")

    print(f"Publishing documents to '{output_bucket}' bucket...")
    print("Press Ctrl+C to stop.")

    try:
        while last_index < len(data):

            doc_content = []
            for item in data[last_index : last_index + offset]:
                doc_content.append(item)

            output_filename = f"test_doc_v{chunk_number}.json"

            # Write to MinIO output bucket
            json_bytes = json.dumps(doc_content, indent=2).encode("utf-8")
            minio_client.put_object(
                Bucket=output_bucket,
                Key=output_filename,
                Body=json_bytes,
                ContentType="application/json",
            )

            last_index += offset
            chunk_number += 1
            print(
                f"JSON doc file successfully written to '{output_bucket}/{output_filename}'\n"
            )
            time.sleep(random.randint(3,10)) 

    except KeyboardInterrupt:
        print("\nStopping docs publisher.")
    except Exception as e:
        print(f"Error during processing: {e}")
    finally:
        print("docs producer closed.")


if __name__ == "__main__":
    generating_json_docs()
