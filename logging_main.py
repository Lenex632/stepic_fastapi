import uvicorn

from fastapi import FastAPI
from loguru import logger

app = FastAPI()

logger.add("info.log")


@app.get("/{name}")
async def main_page(name):
    logger.info("Hello from the root path")
    hello_world()
    return {"message": f"Hello {name}"}


def hello_world():
    logger.info("hello() called!")


if __name__ == "__main__":
    uvicorn.run("logging_main:app", host="127.0.0.1", port=8000, reload=True)

