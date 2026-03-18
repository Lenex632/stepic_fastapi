import time

import uvicorn
from celery import Celery
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()

celery = Celery(
    __name__,
    broker='redis://127.0.0.1:6379/0',
    backend='redis://127.0.0.1:6379/0',
    broker_connection_retry_on_startup=True
)


@celery.task
def call_background_task(message):
    time.sleep(10)
    print("Background Task called!")
    print(message)


@app.get("/")
async def hello_world(message: str):
    call_background_task.delay(message)
    return {'message': 'Hello World!'}


if __name__ == "__main__":
    uvicorn.run("celery_main:app", host="127.0.0.1", port=8000, reload=True)

