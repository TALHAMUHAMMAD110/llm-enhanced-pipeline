from dotenv import load_dotenv
import boto3
from io import BytesIO
from sqlalchemy import create_engine
from pymongo import MongoClient
from config import *


load_dotenv()


def minio_client():
    minio_client = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=MINIO_ROOT_USER,
        aws_secret_access_key=MINIO_ROOT_PASSWORD,
        region_name="us-east-1",
    )
    return minio_client


def postgres_client():
    engine = create_engine(
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )
    return engine


def mongo_client():

    client = MongoClient(MONGO_URI)

    return client
