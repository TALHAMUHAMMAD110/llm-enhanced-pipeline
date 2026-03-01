import time

from client import postgres_client, mongo_client
from lambda_extract import extracting_files_from_bucket
from helper import reading_files_from_bucket
import pandas as pd
import os
from config import *
from lambda_transform import (
    processed_doc,
    llm_processing,
    process_monitoring_doc,
    flattened_doc,
)


def load_data_to_postgres(df, table_name):
    engine = postgres_client()
    df.to_sql(
        table_name,
        engine,
        if_exists="append",
        index=False,
    )
    print(f"Data saved to PostgreSQL table '{table_name}' with shape {df.shape}")


def load_processed_data_to_mongo(processed_doc):
    mongo_engine = mongo_client()
    db = mongo_engine[MONGO_DB]
    collection = db[MONGO_COLLECTION]
    collection.insert_one(processed_doc)
    print(f"Inserted processed document ID {processed_doc['document_id']} into MongoDB")


def processing_files_and_loading():
    input_bucket = os.getenv("INPUT_BUCKET", "docs-bucket")
    files_names = extracting_files_from_bucket()

    flattened_df_list = []
    df_list_monitoring = []

    for file_name in files_names:
        docs = reading_files_from_bucket(input_bucket, file_name)
        print(f"Processing file: {file_name} with {len(docs)} documents")

        for doc in docs:
            processed = processed_doc(doc)
            flattened = flattened_doc(processed)
            llm_processed = llm_processing(processed)
            monitoring_doc = process_monitoring_doc(llm_processed, len(files_names))
            df_list_monitoring.append(monitoring_doc)
            flattened_df_list.extend(flattened)

            load_processed_data_to_mongo(processed)
            print(f"Successfully processed document ID: {processed['document_id']}")

    if len(flattened_df_list) > 0:
        flattened_df = pd.DataFrame(flattened_df_list)
        flattened_df = flattened_df.sort_values(by=["document_id"])
        load_data_to_postgres(flattened_df, "sales")
        print(
            f"sales documents laod to database with shape with {flattened_df.shape[0]} rows"
        )
    else:
        print("No sales documents processed or load to database...")

    if len(df_list_monitoring) > 0:
        monitoring_df = pd.DataFrame(df_list_monitoring)
        monitoring_df = monitoring_df.sort_values(by=["document_id"])
        load_data_to_postgres(monitoring_df, "monitoring")
    else:
        print("No monitoring documents processed or load to database...")


if __name__ == "__main__":
    while True:
        print("Checking for new files to process...")
        processing_files_and_loading()
        time.sleep(10)
