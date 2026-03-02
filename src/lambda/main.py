from lambda_load import processing_files_and_loading
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)


def main():
    while True:
        logging.info("Checking for new files to process...")

        docs_count = processing_files_and_loading()

        logging.info(f"Processed and loaded {docs_count} documents successfully.")
        time.sleep(10)


if __name__ == "__main__":
    main()
