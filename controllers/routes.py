from fastapi import APIRouter, HTTPException
from services.services import download_and_load_data
import uuid

router = APIRouter()

REPORTS = {}


@router.post("/trigger_report")
def trigger_report():
    report_id = str(uuid.uuid4())
    REPORTS[report_id] = "Running"
    return {"report_id": report_id}


@router.get("/get_report")
def get_report(report_id: str):
    status = REPORTS.get(report_id)
    if status == "Running":
        return {"status": "Running"}
    elif status == "Complete":
        pass
    else:
        raise HTTPException(status_code=404, detail="Report not found")
