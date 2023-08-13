import csv

import gdown
import requests
import logging
from models.models import StoreStatus, BusinessHours, StoreTimezone
from db.db import SessionLocal

logging.basicConfig(level=logging.INFO)

URL1 = 'https://drive.google.com/file/d/1UIx1hVJ7qt_6oQoGZgb8B3P2vd1FD025/view?usp=sharing'
URL2 = 'https://drive.google.com/file/d/1va1X3ydSh-0Rt1hsy2QSnHRA4w57PcXg/view?usp=sharing'
URL3 = 'https://drive.google.com/file/d/101P9quxHoMZMZCVWQ5o-shonk2lgK1-o/view?usp=sharing'


def download_and_load_data():
    logging.info('Starting download and load process.')
    download_and_load(URL1, StoreStatus, ['store_id', 'timestamp_utc', 'status'])
    download_and_load(URL2, BusinessHours, ['store_id', 'day', 'start_time_local', 'end_time_local'])
    download_and_load(URL3, StoreTimezone, ['store_id', 'timezone_str'])
    logging.info('Download and load process completed.')


def download_and_load(url, model_class, columns):
    logging.info(f"Downloading from {url}")
    file_id = url.split('/')[-2]
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    output_file_path = 'temp.csv'
    gdown.download(download_url, output_file_path, quiet=False)
    logging.info("Download completed. Reading CSV.")

    with open(output_file_path, 'r') as file:
        reader = csv.DictReader(file)
        logging.info("CSV reader initialized. Connecting to DB.")

        with SessionLocal() as db:
            logging.info("DB connected. Processing rows.")
            for row in reader:
                print(row)
                model_data = {key: row[key] for key in columns if key in row}
                instance = model_class(**model_data)
                db.add(instance)
            logging.info("Rows processed. Committing to DB.")
            db.commit()

    logging.info("Process completed for this URL.")