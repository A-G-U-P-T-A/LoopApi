import csv
from uuid import uuid4

import gdown
import requests
import logging
from models.models import StoreStatus, BusinessHours, StoreTimezone, ReportStatus, GeneratedReport
from db.db import SessionLocal, clear_tables, init_db

logging.basicConfig(level=logging.INFO)

URL1 = 'https://drive.google.com/file/d/1UIx1hVJ7qt_6oQoGZgb8B3P2vd1FD025/view?usp=sharing'
URL2 = 'https://drive.google.com/file/d/1va1X3ydSh-0Rt1hsy2QSnHRA4w57PcXg/view?usp=sharing'
URL3 = 'https://drive.google.com/file/d/101P9quxHoMZMZCVWQ5o-shonk2lgK1-o/view?usp=sharing'


def download_and_load_data():
    init_db()
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


def create_report_status():
    report_id = str(uuid4())
    with SessionLocal() as db:
        db.add(ReportStatus(report_id=report_id))
        db.commit()
    return report_id


def update_report_status(report_id, status):
    with SessionLocal() as db:
        report_status = db.query(ReportStatus).filter(ReportStatus.report_id == report_id).first()
        report_status.status = status
        db.commit()


def get_report_status(report_id):
    with SessionLocal() as db:
        return db.query(ReportStatus).filter(ReportStatus.report_id == report_id).first()


def save_generated_report(report_id, report_data):
    with SessionLocal() as db:
        db.add(GeneratedReport(report_id=report_id, report_data=report_data))
        db.commit()


def get_generated_report(report_id):
    with SessionLocal() as db:
        return db.query(GeneratedReport).filter(GeneratedReport.report_id == report_id).first()


def generate_report_async(report_id):
    # Set the status to running
    with SessionLocal() as db:
        status = db.query(ReportStatus).filter(ReportStatus.report_id == report_id).first()
        status.status = 'running'
        db.commit()

    # Generate the report here according to the specifications
    # ...
    report_data = {
        'store_id': '123',
        'uptime_last_hour': 50.0,
        'uptime_last_day': 12.0,
        'update_last_week': 80.0,
        'downtime_last_hour': 10.0,
        'downtime_last_day': 2.0,
        'downtime_last_week': 5.0
    }
    # Save the report and update the status to complete
    with SessionLocal() as db:
        db.add(GeneratedReport(report_id=report_id, report_data=report_data))
        status = db.query(ReportStatus).filter(ReportStatus.report_id == report_id).first()
        status.status = 'complete'
        db.commit()


def clear_db_data():
    clear_tables()
