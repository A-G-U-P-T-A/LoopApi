from fastapi import FastAPI
from controllers.routes import router
from services.services import download_and_load_data, download_and_load
from apscheduler.schedulers.background import BackgroundScheduler


def poll_and_load_first_dataset():
    download_and_load_data()


def startup_data_load():
    download_and_load_data()


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    scheduler = BackgroundScheduler()
    scheduler.add_job(poll_and_load_first_dataset, 'interval', hours=1)
    scheduler.start()
    startup_data_load()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080)
