from fastapi import FastAPI
import uvicorn

from app.routers import categories, products, users


app = FastAPI(
    title="Тестовый интернет магазин",
    version="0.1.0"
)

app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)


@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "Добро пожаловать в API интернет-магазина!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

