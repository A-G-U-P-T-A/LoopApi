from fastapi import APIRouter
from services.services import get_report_status, get_generated_report, create_report_status, \
    generate_report_async
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

router = APIRouter()


@router.post("/trigger_report")
def trigger_report():
    report_id = create_report_status()
    future = executor.submit(generate_report_async, report_id)
    return {"report_id": report_id}


@router.get("/get_report")
def get_report(report_id: str):
    status = get_report_status(report_id)
    if status and status.status == 'complete':
        report = get_generated_report(report_id)
        return {"status": "Complete", "report": report.report_data}
    elif status:
        return {"status": status.status}
    else:
        return {"status": "Not Found"}
