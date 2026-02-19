from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, EmailStr, PositiveInt, NonNegativeInt, SecretStr
from datetime import datetime
from decimal import Decimal
from typing import Annotated


app = FastAPI()


class MessageCreate(BaseModel):
    content: str


class Message(BaseModel):
    id: int
    content: str


class User(BaseModel):
    username: str = Field(min_length=3, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(..., description="Электронная почта пользователя")
    is_active: bool = Field(default=True, description="Статус активности пользователя")


class Task(BaseModel):
    title: str = Field(min_length=3, max_length=100, description="Название задачи")
    description: str | None = Field(default=None, max_length=500, description="Описание задачи")
    is_completed: bool = Field(default=False, description="Статус завершения задачи")


class Order(BaseModel):
    order_id: PositiveInt = Field(..., description="Уникальный идентификатор заказа")
    user_id: PositiveInt = Field(..., description="Идентификатор пользователя, сделавшего заказ")
    total_amount: Decimal = Field(..., ge=0, description="Общая сумма заказа")
    created_at: datetime = Field(..., description="Дата и время создания заказа")


class Address(BaseModel):
    user_id: PositiveInt = Field(description="Идентификатор пользователя")
    city: str = Field(min_length=2, max_length=100, description="Город")
    street: str = Field(min_length=2, max_length=200, description="Улица")
    postal_code: int = Field(ge=10100, le=99999, description="Почтовый индекс")


class Product(BaseModel):
    product_slug: str = Field(min_length=3, max_length=120, pattern="^[a-zA-Z0-9_-]+$", description="Слаг продукта")
    name: str = Field(min_length=3, max_length=100, description="Название продукта")
    price: Decimal = Field(gt=0, description="Цена продукта")
    stock: NonNegativeInt = Field(default=0, description="Количество продукта на складе")


class Post(BaseModel):
    author_id: Annotated[PositiveInt, Field(description="Идентификатор автора")]
    title: Annotated[str, Field(max_length=100, description="Заголовок записи, не более 100 символов")]
    description: Annotated[str | None, Field(max_length=250, description="Описание записи, не более 250 символов")] = None
    content: Annotated[str, Field(description="Контент записи")]
    created_at: Annotated[datetime, Field(default_factory=datetime.now, description="Запись создана")]
    upadted_at: Annotated[datetime | None, Field(description="Запись обновлена")] = None
    is_published: Annotated[bool, Field(description="Запись опубликована")] = False
    tags: Annotated[list[str], Field(description="Теги записи")] = []


class User(BaseModel):
    username: Annotated[str, Field(min_length=5, max_length=20, description="Пользовательское имя, от 5 до 20 символов")]
    password: Annotated[SecretStr, Field(min_length=8, max_length=50, description="Пароль, от 8 до 50 символов")]
    email: Annotated[EmailStr, Field(description="Электронная почта")]
    first_name: Annotated[str | None, Field(min_length=2, max_length=30, description="Имя, от 2 до 30 символов")] = None
    last_name: Annotated[str | None, Field(min_length=2, max_length=30, description="Фамилия, от 2 до 30 символов")] = None
    is_active: Annotated[bool, Field(description="Учётная запись активна")] = True
    is_staff: Annotated[bool, Field(description="Является служебным пользователем")] = False
    is_superuser: Annotated[bool, Field(description="Является суперпользователем")] = False
    date_joined: Annotated[datetime, Field(default_factory=datetime.now, description="Зарегистрирован")]
    last_login: Annotated[datetime | None, Field(description="Последнее посещение")] = None


messages_db: list[Message] = [Message(id=0, content="First post in FastAPI")]


@app.get("/messages", response_model=list[Message])
async def read_messages() -> list[Message]:
    return messages_db


@app.get("/messages/{message_id}", response_model=Message)
async def read_message(message_id: int) -> Message:
    for message in messages_db:
        if message.id == message_id:
            return message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")


@app.post("/messages", response_model=Message, status_code=status.HTTP_201_CREATED)
async def create_message(message_create: MessageCreate) -> Message:
    next_id = max((msg.id for msg in messages_db), default=-1) + 1
    new_message = Message(id=next_id, content=message_create.content)
    messages_db.append(new_message)
    return new_message


@app.put("/messages/{message_id}", response_model=Message)
async def update_message(message_id: int, message_create: MessageCreate) -> Message:
    for i, message in enumerate(messages_db):
        if message.id == message_id:
            updated_message = Message(id=message_id, content=message_create.content)
            messages_db[i] = updated_message
            return updated_message
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")


@app.delete("/messages/{message_id}", status_code=status.HTTP_200_OK)
async def delete_message(message_id: int) -> dict:
    for i, message in enumerate(messages_db):
        if message.id == message_id:
            messages_db.pop(i)
            return {"detail": f"Message ID={message_id} deleted!"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Message not found")


@app.delete("/messages", status_code=status.HTTP_200_OK)
async def delete_messages() -> dict:
    messages_db.clear()
    return {"detail": "All messages deleted!"}

