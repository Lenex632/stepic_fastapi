from fastapi import FastAPI, Body, status, HTTPException


app = FastAPI()
comments_db = {0: "First comment in FastAPI"}


@app.get("/comments")
async def get_notes() -> dict:
    return comments_db


@app.get("/comments/{comment_id}")
async def get_task(comment_id: int):
    try:
        return comments_db[comment_id]
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")


@app.post("/comments", status_code=status.HTTP_201_CREATED)
async def create_message(comment: str = Body(...)) -> str:
    current_index = max(comments_db) + 1 if comments_db else 0
    comments_db[current_index] = comment
    return "Comment created!"


@app.put("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def update_quote(comment_id: int, comment: str = Body(...)) -> str:
    if comment_id not in comments_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    comments_db[comment_id] = comment
    return "Comment updated!"


@app.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_message(comment_id: int) -> str:
    if comment_id not in comments_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    comments_db.pop(comment_id)
    return "Comment deleted!"

