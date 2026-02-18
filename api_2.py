from fastapi import FastAPI, Path, Query
from typing import Annotated


app = FastAPI()

UserValidator = Annotated[str, Path(min_length=3, max_length=15, description="Enter your username", examples=["Ilya"])]
AgeValidator = Annotated[int, Path(ge=0, le=100, description="Enter your age")]
QueryValidator = Annotated[str | None, Query(max_length=10)]
ListValidator = Annotated[
    list[str],
    Query(min_length=1, max_length=5, description="List of user names", example=["Tom", "Sam"])
]


@app.get("/user1/{username}/{age}")
async def login1(username: UserValidator, age: AgeValidator) -> dict:
    return {"user": username, "age": age}


@app.get("/user2/{username}")
async def login2(username: UserValidator, age: int) -> dict:
    return {"user": username, "age": age}


@app.get("/user/{username}")
async def login(username: UserValidator, first_name: QueryValidator = None) -> dict:
    return {"user": username, "Name": first_name}


@app.get("/user")
async def search(people: ListValidator) -> dict:
    return {"user": people}


UserNameValidator = Annotated[str, Path(min_length=4, max_length=20, description="Enter your name")]


@app.get("/users/{name}")
async def get_user(name: UserNameValidator) -> dict:
    return {"user_name": name}


CategoryValidator = Annotated[int, Path(gt=0, description="Category ID")]


@app.get("/category/{category_id}/products")
async def category(category_id: CategoryValidator, page: int) -> dict:
    return {"category_id": category_id, "page": page}

