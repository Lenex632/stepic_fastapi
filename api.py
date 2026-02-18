from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def welcome() -> dict:
    return {"message": "Hello, FastAPI!"}


@app.get("/hello/{user}")
async def welcome_user(user: str) -> dict:
    return {"user": f"Hello {user}"}


@app.get("/product")
async def detail_view(item_id: int) -> dict:
    return {"product": f"Stock number {item_id}"}


@app.get("/products/{product_id}")
async def detail_view1(product_id: int) -> dict:
    return {"product": f"Stock number {product_id}"}


@app.get("/users/admin")
async def admin() -> dict:
    return {"message": "Hello admin"}


@app.get("/users")
async def users(name: str, age: int) -> dict:
    return {"user_name": name, "user_age": age}


@app.get("/users/{name}")
async def users2(name: str) -> dict:
    return {"user_name": name}


@app.get("/users/{name}/{age}")
async def users1(name: str, age: int) -> dict:
    return {"user_name": name, "user_age": age}

