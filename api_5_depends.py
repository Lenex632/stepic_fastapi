from fastapi import FastAPI, Depends, Query, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

# ---------------------------------------------------------------------------------


async def pagination_func(limit: int = Query(10, ge=0), page: int = 1):
    return [{'limit': limit, 'page': page}]


@app.get("/messages")
async def all_messages(pagination: list = Depends(pagination_func)):
    return {"messages": pagination}


@app.get("/comments")
async def all_comments(pagination: list = Depends(pagination_func)):
    return {"comments": pagination}

# ---------------------------------------------------------------------------------


class Post(BaseModel):
    id: int
    text: str


db = []


async def get_post_or_404(id: int):
    try:
        return db[id]
    except IndexError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get("/message/{id}")
async def get_message1(post: Post = Depends(get_post_or_404)):
    return post


@app.post("/message", status_code=status.HTTP_201_CREATED)
async def create_message(post: Post) -> str:
    post.id = len(db)
    db.append(post)
    return "Message created!"

# ---------------------------------------------------------------------------------


async def get_message():
    return "Hello from dependency!"


@app.get("/welcome")
async def welcome(message: str = Depends(get_message)) -> dict:
    return {"message": message}

# ---------------------------------------------------------------------------------


async def check_auth(token: str):
    if token == "secret":
        return True
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/profile")
async def auth(is_ok=Depends(check_auth)) -> str:
    return "User is authorized"

